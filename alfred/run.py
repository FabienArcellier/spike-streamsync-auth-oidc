import alfred

@alfred.command("run", help="execute the application")
def run():
    """
    execute the application

    >>> $ alfred run
    """
    streamsync = alfred.sh("streamsync", "streamsync should be present")
    alfred.run(streamsync, ['run', 'src/app'])


@alfred.command("edit", help="design the application")
@alfred.option("--remote", help="enable edition through public connection", is_flag=True)
def edit(remote: bool = False):
    """
    execute the application in edition mode

    >>> $ alfred edit
    """
    args = []
    if remote:
        args.append('--enable-remote-edit')
    args += ['edit', 'src/app']

    streamsync = alfred.sh("streamsync", "streamsync should be present")
    alfred.run(streamsync, args)
