const { DateTime } = require('luxon');
const fs = require('fs');
const pluginRss = require('@11ty/eleventy-plugin-rss');
const pluginSyntaxHighlight = require('@11ty/eleventy-plugin-syntaxhighlight');
const pluginNavigation = require('@11ty/eleventy-navigation');
const markdownIt = require('markdown-it');
const markdownItAnchor = require('markdown-it-anchor');

module.exports = function (eleventyConfig) {
  // ✅ Add plugins
  eleventyConfig.addPlugin(pluginRss);
  eleventyConfig.addPlugin(pluginSyntaxHighlight);
  eleventyConfig.addPlugin(pluginNavigation);

  // ✅ Define site URL (for sitemap & absolute URLs)
  eleventyConfig.addGlobalData("site.url", "https://www.nillianstore.com");

  // ✅ Merge data deeply
  eleventyConfig.setDataDeepMerge(true);

  // ✅ Layout aliases
  eleventyConfig.addLayoutAlias('post', 'layouts/post.njk');
  eleventyConfig.addLayoutAlias('shop', 'layouts/shop.njk');

  // ✅ Filters
  eleventyConfig.addFilter('readableDate', (dateObj) => {
    return DateTime.fromJSDate(dateObj, { zone: 'utc' }).toFormat('dd LLL yyyy');
  });

  eleventyConfig.addFilter('htmlDateString', (dateObj) => {
    return DateTime.fromJSDate(dateObj, { zone: 'utc' }).toFormat('yyyy-LL-dd');
  });

  // ISO 8601 datetime with timezone for schema.org
  eleventyConfig.addFilter('isoDateTime', (dateObj) => {
    return DateTime.fromJSDate(dateObj, { zone: 'Asia/Dubai' }).toISO();
  });

  eleventyConfig.addFilter('head', (array, n) => {
    if (n < 0) return array.slice(n);
    return array.slice(0, n);
  });

  eleventyConfig.addFilter('min', (...numbers) => {
    return Math.min.apply(null, numbers);
  });

  // Safe slug filter: normalizes using Eleventy's slug filter then removes any HTML entities
  // and unsafe characters (e.g., #, ?, apostrophes) so filenames are valid on Netlify.
  const eleventySlug = eleventyConfig.getFilter('slug');
  eleventyConfig.addFilter('safeSlug', function (str) {
    if (!str) return '';
    // Use existing slug filter first
    let s = eleventySlug(String(str));
    // Decode common HTML entity variants for apostrophe and ampersand-encoded forms
    s = s.replace(/&amp;#39;|&#39;|&apos;|['’`]/g, '');
    // Remove any remaining characters that are not a-z, 0-9 or hyphen
    s = s.toLowerCase().replace(/[^a-z0-9\-]/g, '-');
    // Collapse multiple hyphens and trim
    s = s.replace(/-+/g, '-').replace(/(^-|-$)/g, '');
    return s;
  });

  eleventyConfig.addFilter('filterTagList', (tags) => {
    return (tags || []).filter(tag => ['all', 'nav', 'post', 'posts', 'shop', 'shops'].indexOf(tag) === -1);
  });

  eleventyConfig.addFilter("sanitize", function (str) {
  return str.replace(/"/g, "'").replace(/\n/g, " ").trim();
});

  // ✅ Collections
  // Create a collection for all shop products
eleventyConfig.addCollection("tagList", function(collection) {
  const tagMap = new Map();

  collection.getAll().forEach(item => {
    if (!item.data.tags) return;

    let tags = item.data.tags;
    if (typeof tags === "string") tags = [tags];

    tags.forEach(tag => {
      // Use safeSlug here so the collection keys match the sanitized permalinks
      const slug = eleventyConfig.getFilter("safeSlug")(tag);
      if (!tagMap.has(slug)) {
        tagMap.set(slug, tag);
      }
    });
  });

  return Array.from(tagMap.values()).filter(
    tag => !["all", "nav", "post", "posts", "shop", "shops"].includes(tag)
  );
});



  // ✅ Passthrough copy
  eleventyConfig.addPassthroughCopy('img');
  eleventyConfig.addPassthroughCopy('css');
  eleventyConfig.addPassthroughCopy('robots.txt');
  eleventyConfig.addPassthroughCopy('feed');
  eleventyConfig.addPassthroughCopy('videos');
  eleventyConfig.addPassthroughCopy('_headers');

  // ✅ Markdown library
  let markdownLibrary = markdownIt({
    html: true,
    breaks: true,
    linkify: true,
  }).use(markdownItAnchor, {
    permalink: true,
    permalinkClass: 'direct-link',
    permalinkSymbol: '#',
  });
  eleventyConfig.setLibrary('md', markdownLibrary);

  // ✅ Browsersync middleware
  eleventyConfig.setBrowserSyncConfig({
    callbacks: {
      ready: function (err, browserSync) {
        const content_404 = fs.readFileSync('_site/404.html');
        browserSync.addMiddleware('*', (req, res) => {
          res.writeHead(404, { 'Content-Type': 'text/html; charset=UTF-8' });
          res.write(content_404);
          res.end();
        });
      },
    },
    ui: false,
    ghostMode: false,
  });

  // Add XML encoding filter
eleventyConfig.addFilter('xmlEncode', function(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '<')
    .replace(/>/g, '>')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
});

  // ✅ Return config
  return {
    templateFormats: ['md', 'njk', 'html', 'liquid'],
    pathPrefix: '/',
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: false,
    dir: {
      input: '.',
      includes: '_includes',
      data: '_data',
      output: '_site',
    },
  };
};
