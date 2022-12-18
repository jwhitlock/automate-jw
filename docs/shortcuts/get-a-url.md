# Shortcut: Get a URL

Looks for an URL in Safari or on the clipboard, loading into variable **urls**

* If one is found, use it.
* If multiple are found, ask which ones to use
* If none are found, ask for a URL

Output result.

## Status
* Getting a URL from Safari might not work
* Getting a URL from clipboard works well
* Getting a URL from dialog works, but trimming looks weird

## Commands

Commands are plain text, variables are **in bold**, multiple variables are **split** `_` **with an underscore**.

* Find **All Windows** where
    **App Name** `_` **is** `_` **Safari**
    Sort by **Window Index**
    Order **Smallest First**
* If **Windows** `_` **has any value**
    * Get current web page fro Safari
    * Add **Page URL** to **urls**
* End If
* Get clipboard
* Get URLS for **Clipboard**
* If **URLs** `_` **has any value**
    * Add **URLs** to **urls**
* End If
* Count **Items** in **urls**
* If **Count** `_` **is less than** `_` **1**
    * Ask for **URL** with **What URL?**
      Default URL: None
    * Set variable **url** to **Provided Input**
* Otherwise
    * If **Count** `_` **is greater than** `_` **1**
        * List
          **urls**
        * Choose from **List**
          Prompt **Which URL?**
          Select multiple ✓
        * Set variable **url** to **urls**
    * Otherwise
        * Set variable **url** to **urls**
    * End if
* End if
* Stop and output **If Result**
  If there's nowhere to output:
  **Do Nothing**
