import asyncio
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from textual.app import App

from unctl.config.config import load_config, set_config_instance
from unctl.constants import CheckProviders
from unctl.interactive.interactive import InteractiveApp
from unctl.interactive.remediation import RemediationApp
from unctl.lib.checks.loader import ChecksLoader
from unctl.lib.display.display import Displays
from unctl.lib.llm.assistant import OpenAIAssistant
from unctl.lib.llm.utils import set_llm_instance
from unctl.list import load_checks, get_categories, get_services
from unctl.scanrkube import JobDefinition, ResourceChecker, DataCollector
from unctl.version import check, current

LLM_ANALYSIS_THRESHOLD = 10


def unctl_process_args(argv=None):
    parser = ArgumentParser(
        prog="unctl",
        description="\n\t  Welcome to unSkript CLI Interface \n",
        formatter_class=RawTextHelpFormatter,
        epilog="""
To see the different available options on a specific provider, run:
    unctl {provider} -h|--help
""",
    )
    common_parent_parser = ArgumentParser(add_help=False)

    subparsers = parser.add_subparsers(
        title="unctl available providers", dest="provider"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=current(),
    )

    common_parent_parser.add_argument(
        "-s",
        "--scan",
        help="Run a provider scan",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "-e",
        "--explain",
        help="Explain failures using AI",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "-f",
        "--failing-only",
        help="Show only failing checks",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "-c",
        "--checks",
        help="Filter checks by IDs",
        nargs="+",
    )
    common_parent_parser.add_argument(
        "--sort-by",
        choices=["object", "check"],
        default="object",
        help="Sort results by 'object' (default) or 'check'",
    )
    common_parent_parser.add_argument(
        "--categories",
        help="Filter checks by category",
        nargs="+",
        default=None,
    )
    common_parent_parser.add_argument(
        "--services",
        help="Filter checks by services",
        nargs="+",
        default=None,
    )
    common_parent_parser.add_argument(
        "-l",
        "--list-checks",
        help="List available checks",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "--no-interactive",
        default=False,
        help="Interactive mode is not allowed. Prompts will be skipped",
    )
    common_parent_parser.add_argument(
        "--list-categories",
        help="List available categories",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "--list-services",
        help="List available services",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "-d",
        "--diagnose",
        help="Run fixed diagnosis",
        action="store_true",
    )
    common_parent_parser.add_argument(
        "-r",
        "--remediate",
        help="Create remediation plan",
        action="store_true",
    )
    parser.add_argument(
        "--config",
        help="Specify path to the unctl config file",
        nargs="+",
        default=None,
    )

    # todo: for now both k8s and mysql share the same CLI args
    # todo: should be separated, as its unlikely that both k8s and mysql have equal args
    subparsers.add_parser(name=CheckProviders.K8S.value, parents=[common_parent_parser])
    subparsers.add_parser(
        name=CheckProviders.MySQL.value, parents=[common_parent_parser]
    )

    args = parser.parse_args(args=argv)
    if len(sys.argv) <= 2:
        parser.print_help()
        sys.exit(0)

    return args


def prompt_interactive(options, app: App):
    if not options.no_interactive:
        choice = input("Do You want enter interactive mode to continue? (Y/n)\n> ")
        if choice != "n":
            app.run()


def _get_app(options, display=None):
    llm_helper = None
    if options.explain or options.remediate:
        try:
            llm_helper = OpenAIAssistant(options.provider)
        except Exception as e:
            sys.exit("Failed to initialize LLM: " + str(e))

    set_llm_instance(llm_helper)
    display = display or Displays.get_display(options.provider)
    loader = ChecksLoader()
    check_modules = loader.load_all(
        provider=options.provider,
        categories=options.categories,
        services=options.services,
        checks=options.checks,
    )
    # Create a job definition
    job_definer = JobDefinition(check_modules)
    jobs = job_definer.generate_jobs()
    print("✅ Created jobs")

    # collect inventory
    collector = DataCollector.make_collector(options.provider)
    print("✅ Collected Kubernetes data")

    app = ResourceChecker(display, collector, jobs, options.provider)
    return app


def unctl(options):
    display = Displays.get_display(options.provider)
    display.init(options)

    if options.list_checks:
        checks_metadata = load_checks(
            provider=options.provider,
            categories=options.categories,
            services=options.services,
            checks=options.checks,
        )
        display.display_list_checks_table(checks_metadata)
        sys.exit()

    if options.list_categories:
        categories = get_categories(provider=options.provider)
        display.display_grouped_data("Category", categories)
        sys.exit()

    if options.list_services:
        services = get_services(provider=options.provider)
        display.display_grouped_data("Service", services)
        sys.exit()

    app = _get_app(options, display=display)
    interactive_app = InteractiveApp(
        provider=options.provider,
        checker=app,
    )

    results = asyncio.run(app.execute())

    if not options.explain and not options.remediate:
        # explanations not needed: print and exit
        display.display_results_table(results, sort_by=options.sort_by)
        prompt_interactive(options=options, app=interactive_app)
        return results, app.failing_reports, None

    if len(app.failing_reports) > LLM_ANALYSIS_THRESHOLD:
        choice = input(
            f"unctl found {len(app.failing_reports)} failed items in your system. "
            "It will start sessions at LLM service for each of the item. "
            "Do You still want to use LLM to explain all the failures? (Y/n)\n> "
        )
        if choice == "n":
            display.display_results_table(results, sort_by=options.sort_by)
            prompt_interactive(options=options, app=interactive_app)
            return results, app.failing_reports, None

    # for each failure, print out the summary
    # and the recommendations
    print("\n\n🤔 Running diagnostic commands...\n")
    asyncio.run(app.diagnose())
    print("🤔 Analyzing results...\n")
    asyncio.run(app.analyze_results())

    display.display_results_table(results, llm_summary=True, sort_by=options.sort_by)

    if not options.remediate:
        prompt_interactive(options=options, app=interactive_app)
        return results, app.failing_reports, None

    if options.remediate:
        asyncio.run(app.find_dependencies())
        RemediationApp(
            provider=options.provider,
            checker=app,
        ).run()

        return results, app.failing_reports, app.failure_groups


def main(argv=None):
    # check version and notify if new version released
    check()

    options = unctl_process_args(argv)
    app_config = load_config(options.config)
    set_config_instance(app_config)

    unctl(options)


if __name__ == "__main__":
    sys.exit(main())
