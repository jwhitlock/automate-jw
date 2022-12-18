# automate-jw: Automate jwhitlock

This project is a set of scripts and documentation for automating my task
workflow. My goal is to have a keyboard shortcut that says:

    "Do what I normally do with what I'm currently seeing"

Often, "what I see" is a webpage in Safari or Firefox, and "what I normally do"
is add a task to [OmniFocus][], which I use for personal project management. I
use Apple stuff (macOS, iPhone, etc.), which includes automation tools like
[Shortcuts][], so it should be possible to encode the rules for what I'd like
to do.

[OmniFocus]: https://www.omnigroup.com/omnifocus
[Shortcuts]: https://support.apple.com/guide/shortcuts-mac

## Status

I've got a "read later" workflow for Substack article:

* Open the article on substack
* Copy the URL to the clipboard
* Run "Send Article to Omnifocus" shortcut
    - "Get A URL" gets URL from Clipboard
    - URL is passed to `automate-jw-process-url` script, installed in virtual environment.
    - Script returns base64-encoded JSON
    - Omni Automation decodes to JSON, creates a task

### To Do

* Sketch the planned workflow
* Split out Omnifocus task creation as own Shortcut
* Document the Shortcut and OmniFocus automation script
* Add References section
* Sketch semantic scraper ideas
* Implement semantic scraper

## Documentation
* [Overview](docs/overview.md) - Overview of the workflow
* Shortcuts
    - [Get a URL](docs/shortcuts/get-a-url.md) - Gets a URL from Safari or the Clipboard
    - [Send URL to Omnifocus](docs/shortcuts/send-url-to-omnifocus.md) - Processes a URL, creates an OmniFocus task
