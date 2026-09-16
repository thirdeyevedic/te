// @ts-check
import { defineConfig } from 'astro/config';
import sitemap, { ChangeFreqEnum } from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://thirdeyeevents.com',
  trailingSlash: 'ignore',
  integrations: [
    sitemap({
      filter: (page) => !/\/(privacy|terms|sitemap)\/?$/.test(page),
      /* `SitemapItem['changefreq']` is the `EnumChangefreq` enum, not a string
         union — `'monthly'` and friends are rejected by the checker even though
         they are exactly what gets emitted. Use the members the integration
         re-exports instead of casting. */
      serialize(item) {
        const url = item.url;
        let priority = 0.7;
        let changefreq = ChangeFreqEnum.MONTHLY;

        if (url === 'https://thirdeyeevents.com/') {
          priority = 1.0;
          changefreq = ChangeFreqEnum.WEEKLY;
        } else if (
          /^https:\/\/thirdeyeevents\.com\/(weddings|destinations|event-ip|production|about)\/?$/.test(url)
        ) {
          priority = 0.9;
          changefreq = ChangeFreqEnum.MONTHLY;
        } else if (/^https:\/\/thirdeyeevents\.com\/contact\/?$/.test(url)) {
          priority = 0.8;
          changefreq = ChangeFreqEnum.MONTHLY;
        } else if (url.includes('/weddings/experiences/')) {
          priority = 0.6;
          changefreq = ChangeFreqEnum.YEARLY;
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

