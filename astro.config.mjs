// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://thirdeyeevents.com',
  trailingSlash: 'ignore',
  integrations: [
    sitemap({
      filter: (page) => !/\/(privacy|terms|sitemap)\/?$/.test(page),
      serialize(item) {
        const url = item.url;
        let priority = 0.7;
        /** @type {'daily'|'weekly'|'monthly'|'yearly'} */
        let changefreq = 'monthly';

        if (url === 'https://thirdeyeevents.com/') {
          priority = 1.0;
          changefreq = 'weekly';
        } else if (
          /^https:\/\/thirdeyeevents\.com\/(weddings|destinations|event-ip|production|about)\/?$/.test(url)
        ) {
          priority = 0.9;
          changefreq = 'monthly';
        } else if (/^https:\/\/thirdeyeevents\.com\/contact\/?$/.test(url)) {
          priority = 0.8;
          changefreq = 'monthly';
        } else if (url.includes('/weddings/experiences/')) {
          priority = 0.6;
          changefreq = 'yearly';
        }

        return { ...item, changefreq, priority, lastmod: new Date().toISOString().slice(0, 10) };
      },
    }),
  ],
  build: {
    inlineStylesheets: 'auto',
  },
  devToolbar: {
    enabled: false,
  },
});

