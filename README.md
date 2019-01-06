A couple of scripts to play around with Anki internals.

Remember to backup first or risk data loss:

    cp ~/Library/Application\ Support/Anki2/<profile>/collection.anki2 .
    cp collection.anki2{,.bak}

To run, the easiest is to clone Anki sources and run with `PYTHONPATH=<path to Anki repo root>`.
Make sure to read Anki's `README.development` and install all dependencies.
