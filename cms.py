# Simple static site generator for blog posts
# Entries are placed in entries directory. An RSS feed is generated as a side effect.

import glob
import os

from datetime import datetime, timezone

def parse_entry(path):
    with open(path) as f:
        lines = f.readlines()

    title = ""
    created_at = None
    tags = []
    id_ = ""
    content = ""

    for line in lines:
        if line.startswith('title:'):
            title = line[6:].strip()
        elif line.startswith('created_at'):
            print(line[12:].strip())
            created_at = datetime.strptime(line[12:].strip(), '%d/%m/%Y %H:%M')
        elif line.startswith('tags:'):
            tags = line[5:].strip().split(',')
            tags = [tag.strip() for tag in tags]
        elif line.startswith('id:'):
            id_ = line[3:].strip()
        else:
            content += line

    content = content.replace("\n\n", "<br></br>")
    
    return {"title": title, "id": id_, "created_at": created_at, "tags": tags, "content": content}

def parse_entries():
    return [parse_entry(path) for path in glob.glob('entries/**/*.*', recursive=True)]

def build_html(title, meta, body, path):
    depth = len(os.path.relpath(path, start="blog").split(os.sep)) - 1
    relative_path = "../" * depth
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>{title} - megabytesofrem.com</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

      <link rel="stylesheet" type="text/css" href="{relative_path}style/normalize.css">
      <link rel="stylesheet" type="text/css" href="{relative_path}style/style.css">
    </head>
    <body>
      <header class="header">
        <div class="header-inner">
          <div class="menu-icon" id="menu-icon">&#9776;</div>
            <h2>megabytesofrem.com</h2>
          </div>
        <nav class="site-nav" id="site-nav">
          <ul>
            <li><a href="{relative_path}index.html">Home</a></li>
            <li><a href="{relative_path}pages/projects.html">Projects</a></li>
            <li><a href="{relative_path}pages/links.html">Links</a></li>
            <li><a href="{relative_path}pages/blog/index.html" class="curr-page">Blog</a></li>
          </ul>
        </nav>
      </header>

      <div class="page">
        <div class="page-content">
          {body}
        </br>
        <i>Last updated at {str(meta.get('created_at', datetime.today())) if meta is not None else str(datetime.today())}</i>
        </div>
      </div>
      <script src="{relative_path}scripts/nav.js"></script>
    </body>
    </html>
    """

def strip_tags(s):
    # Strip HTML tags out of the index preview
    import re
    stripped = re.sub(re.compile(r'<(.*)>.?|<(.*) />|<|>'), '', s)
    return stripped

def compile_entries():
    os.makedirs("pages/blog", exist_ok=True)
    entries = parse_entries()

    print(f"Compiling {len(entries)} entries...")
    print(entries)
    
    # Generate individual post pages
    for entry in entries:
        depth = len(os.path.relpath(f"pages/blog/{entry['id']}.html", start='pages/blog').split(os.sep)) - 1
        relative_path = '../' * depth

        entry_body = f"""
        <h2>{entry['title']}</h2>
        <h4>{', '.join(['#' + tag for tag in entry['tags']])}</h4>
        <p>{entry['content']}</p>
        <footer>
          <a href="{relative_path}index.html">Return to index</a>
        </footer>
        """
        
        output_path = f"pages/blog/{entry['id']}.html"
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(build_html(entry['title'], entry, entry_body, output_path))
    
    # Generate index page
    index_body = "".join(
        f'''
        <div class="journal-entry">
          <h2><a href="{e["id"]}.html">{e["title"]}</a></h2>
          <h3>{", ".join(["#" + tag for tag in e["tags"]])}</h3>

          <p>{strip_tags(e["content"][:300])}...</p>
        </div>
        '''

        for e in entries
    )

    with open("pages/blog/index.html", 'w') as f:
        f.write(build_html("Posts", None, index_body, "pages/blog/index.html"))

def generate_rss():
    entries = parse_entries()
    rss_items = "".join(
        f"""
        <item>
            <title>{e['title']}</title>
            <link>https://megabytesofrem.com/pages/blog/{e['id']}.html</link>
            <description>{e['content'][:200]}</description>
            <pubDate>{datetime.now(tz=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
        </item>
        """ for e in entries
    )
    rss_feed = f"""
    <?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>megabytesofrem Feed</title>
            <link>https://megabytesofrem.com/pages/blog/</link>
            <description>Latest entries</description>
            {rss_items}
        </channel>
    </rss>
    """
    with open("pages/blog/rss.xml", "w") as f:
        f.write(rss_feed.strip())

if __name__ == '__main__':
    compile_entries()
    generate_rss()
