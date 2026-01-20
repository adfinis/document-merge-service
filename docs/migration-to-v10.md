# Migration to v10

In `v10`, the major change is that we remove all dependency on
[unoconv](https://github.com/unoconv/unoconv) for the following reasons:

First of all, it's been [deprecated](https://github.com/unoconv/unoconv) since
**November 2021**.

Secondly, unoconv was only used to convert our templates directly to a PDF which
is not the main use-case of DMS. However, this integration added most of the
complexity to this project. For this reason, we decided to not migrate to an
alternative (e.g. [unoserver](https://github.com/unoconv/unoserver/)) but to
delegate the PDF conversion to an external service that treats conversion as the
main use-case. Namely, [Gotenberg](https://gotenberg.dev/).

## How to migrate

In order to migrate to v10, a few changes are required. First of all, the
following environment variables can be deleted:

- `UNOCONV_ALLOWED_TYPES`
- `UNOCONV_PYTHON`
- `UNOCONV_PATH`

And if needed, the following block in your compose file as well:

```diff
services:
  document-merge-service:
    image: ghcr.io/adfinis/document-merge-service:dev
-   cap_add:
-     - CAP_SYS_ADMIN
-   security_opt:
-     - apparmor:unconfined
    environment:
      # ...
-     - ISOLATE_UNOCONV=true
```

After this, we can setup and configure gotenberg using docker compose like this:

```diff
services:
  document-merge-service:
    image: ghcr.io/adfinis/document-merge-service:latest
    # ...

+ gotenberg:
+   image: gotenberg/gotenberg:latest
+   environment:
+     # Disable unneeded features
+     - CHROMIUM_DISABLE_ROUTES=true
+     - PDFENGINES_DISABLE_ROUTES=true
+     - WEBHOOK_DISABLE=true
```

For more configuration options, please consult the [Gotenberg
documentation](https://gotenberg.dev/docs/configuration).
