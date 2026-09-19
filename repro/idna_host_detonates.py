import httpx
import httpx._client as c
import httpx._utils

print("--- URL.host with malformed punycode (starts with xn--) ---")
for u in ["http://xn--a.example.com/", "http://xn--e.land/", "http://xn--/p",
          "http://a.xn--b.c/", "http://xn--not-valid-host.test/x"]:
    url = httpx.URL(u)
    try:
        print(f"  {u}: raw_host={url.raw_host!r} host={url.host!r}")
    except Exception as exc:
        print(f"  {u}: raw_host={url.raw_host!r} host -> "
              f"{type(exc).__module__}.{type(exc).__name__}: {exc}")

print("--- str(url) still fine? ---")
u = httpx.URL("http://xn--a.example.com/path")
try:
    print("  str:", str(u), "| repr:", repr(u))
except Exception as exc:
    print("  str ->", type(exc).__name__, exc)

print("--- propagates into redirect helpers (_same_origin / _is_https_redirect use .host) ---")
print("  _same_origin(same punycode host):", end=" ")
try:
    print(c._same_origin(httpx.URL("http://xn--a.example.com/"),
                         httpx.URL("http://xn--a.example.com/")))
except Exception as exc:
    print("->", type(exc).__module__ + "." + type(exc).__name__, ":", exc)
print("  _is_https_redirect:", end=" ")
try:
    print(c._is_https_redirect(httpx.URL("http://xn--a.example.com/"),
                               httpx.URL("https://xn--a.example.com/")))
except Exception as exc:
    print("->", type(exc).__module__ + "." + type(exc).__name__, ":", exc)

print("--- and into URLPattern (proxy/mount matching) ---")
try:
    print("  URLPattern.matches:",
          httpx._utils.URLPattern("all://xn--a.example.com").matches(
              httpx.URL("http://xn--a.example.com/")))
except Exception as exc:
    print("  URLPattern ->", type(exc).__module__ + "." + type(exc).__name__, ":", exc)

print("--- Client._transport_for_url with a mount, malformed punycode URL ---")
try:
    with httpx.Client(mounts={"https://other.com": None}) as client:
        print("  transport_for_url:",
              client._transport_for_url(httpx.URL("http://xn--a.example.com/x")) is client._transport)
except Exception as exc:
    print("  ->", type(exc).__module__ + "." + type(exc).__name__, ":", exc)
