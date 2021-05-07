# Getting up and running

If Conrad--or whoever else assumed this responsibility after him--has passed, fear not: you can probably [contact them in the afterlife](mailto:chstansbury@gmail.com).

Plus, maintaining the website isn't that tricky. The whole thing consists of static HTML and JS content, generated from data files and raw text using [Jekyll](https://jekyllrb.com). Additionally, so you don't tear your hair out, there are a few [custom HTML elements](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements).

Here's what you need to do to get started:

1. Install Jekyll
2. Clone this website
3. Make any necessary changes
4. Ensure that the site looks alright with `bundle exec jekyll serve --incremental`
5. Compile the site with `jekyll build`
6. Push the finished site to the Berkeley FTP server with

```shell script
$> UNFINISHED 
```

## Making Changes

### Team Members

You can just add a .md file in `_members` when new lab members join. Make sure to set their role appropriately so they get sorted into the right section on the page.

When someone leaves, add them to `_data/past_members.yml` and remove the corresponding .md file from `_members`.


### Publications

UNFINISHED

### Items for the Landing Carousel/Flipbook

Put them in `_data/landing_carousel.json`

### Repeated/Templated Content

If you need to add a new type of content that gets repeated a lot, make an HTML Template and custom comoponent, you can have a look at `main.js` and `templates.html` for an example, this way your content is guaranteed to be consistent and there's much much less HTML code floating around.

### Styles

We use [Tailwind CSS](tailwindcss.com), please do not change this to introduce a different CSS framework unless you have a very good reason.