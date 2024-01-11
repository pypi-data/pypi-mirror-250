# Customize

Edit `conf.py` to customize

## Variables

**`html_title`**: Set the title of the document. 

**`html_logo`**: Set the logo image. This should be a relative path to the image from the conf file.

**`html_permalinks_icon`**: Change the permalink symbol (default: ¶)

## Theme variables

**`mochi_navtree_titlesonly`**: If True, only the first heading is included in the sidebar navtree. Defaults to False.

**`mochi_navtree_maxdepth`**: Specifies the maxdepth of navtree. Defaults to -1 (unlimited)


## Sample

```py
html_title = f"{project}"
html_baseurl = ""
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'
html_permalinks_icon = '#'
```

## Note

Note: The content of the left navtree is generated from the `.toctree::` directive in your rst file. Thus, if you omit the documents there, (for example if you used `:titlesonly:` or `:maxdepth: 1`) the subdocuments will never appear in the navtree, regardless of the theme options.

