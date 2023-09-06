import cli , time, sys

# check if any args are missing
if len(sys.argv) < 2:
    try:
        cli.logger.warning("'sentzi-test' accepts arguments . No arguments were given")
        cli.logger.info("For more info try using 'py sentzi-test.py -help'")

        # wait for 20 secs
        for i in range(20,0,-1):
            cli.console.print(f"\t exiting in ( {i} ) s ", end = '\r')
            time.sleep(1)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)

else:
    # execute the CLI tool
    cli.cli(
        prog_name = "sentzi-test"
    )
