<!-- vim: set wrap linebreak breakat&vim: -->
# automate-jw docs

This project is an attempt to automate processing my inboxes. I spend about an hour each workday clearing my email inboxes, catching up on Slack, and reading GitHub activity. I'd like to automate some of this, so that I don't feel I have to monitor my inboxes so closely. Some things I'd like to do:

* Create an OmniFocus task when someone requests a GitHub review
* Create an OmniFocus task when someone assigns me a Jira task

## Shortcuts

* [Get a URL](./shortcuts/get-a-url.md)
* [Send URL to Omnifocus](./shortcuts/send-url-to-omnifocus.md)

## Current Workflow

<!-- Local debugging of Mermaid -->
<!--
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
-->

```mermaid
flowchart TD
  copy_clipboard --> run_sc_send
  run_sc_send --> sc_get_urls
  sc_get_urls --> sc_safari
  sc_safari --> sc_clipboard
  sc_clipboard --> sc_pick_urls
  sc_pick_urls --> sc_process_url
  sc_process_url --> sc_omnifocus_task

  subgraph shortcut_get_a_url [Shortcut: Get a URL]
    sc_safari
    sc_clipboard
    sc_pick_urls
  end

  subgraph shortcut_send_to_omnifocus [Shortcut: Send a URL to Omnifocus]
    sc_get_urls
    sc_process_url
    sc_omnifocus_task
  end

  copy_clipboard[Copy URL to Clipboard]
  run_sc_send["Run shortcut 'Send a URL to Omnifocus'"]
  sc_get_urls["Run shortcut 'Get a URL'"]
  sc_process_url[Run automate-jw-process-url on URL]
  sc_omnifocus_task[Create an OmniFocus task]
  sc_safari[Look for URL in Safari]
  sc_clipboard[Look for URL on clipboard]
  sc_pick_urls["Pick URL(s) to process"]

```
