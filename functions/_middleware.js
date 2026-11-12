// Old Cloudflare Pages addresses (*.pages.dev, including preview builds) send visitors and search engines
// to the main address with a permanent redirect. Everything else is served as usual.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname.endsWith('.pages.dev')) {
    return Response.redirect('https://sericumvia1.sepafshar.com' + url.pathname + url.search, 301);
  }
  return context.next();
}
