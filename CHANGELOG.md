# Changelog

## 8.0.3 (29 September 2025)

### Fix

* **docx-template:** Corruption of libreoffice-originated templates ([`d7b3cec`](https://github.com/adfinis-sygroup/document-merge-service/commit/d7b3cec727457e1f75d1e67d385c9c5d962cca64))

## 8.0.2 (25. July 2025)

### Feature

* **placeholders:** add specific error messages if a "-" is used in a placeholder ([e75252f](https://github.com/adfinis/document-merge-service/commit/e75252fc9d57c4732b23fde8e0143c5908d3bbf5))

### Fix

* **docs:** Correct typo ([58e2d05](https://github.com/adfinis/document-merge-service/commit/58e2d05eb081c397eb0c76494ca6ff7833544e8c))

## 8.0.0 (16. May 2025)

### Feature

* **docker:** Add image variants ([`72fb354`](https://github.com/adfinis/document-merge-service/commit/72fb354aef0f2b4dbd9d1249d2cc6d8df4f30aba))
* **docker:** Replace uwsgi with gunicorn as app server ([`aa3f24b`](https://github.com/adfinis/document-merge-service/commit/aa3f24b7f49c30a4b969ba83f89c522a4779929d))
* **build:** Use multi stage docker build for smaller images ([`73b9e43`](https://github.com/adfinis/document-merge-service/commit/73b9e4351636da53629acd4fe54eb9fba0c2855a))
* **docker:** Use python 3.13 for docker image ([`e38f4a4`](https://github.com/adfinis/document-merge-service/commit/e38f4a4fca21be43d93196ac1675ab223cd1bbdf))
* **deps:** Add python 3.13 to compatibility matrix ([`05e9268`](https://github.com/adfinis/document-merge-service/commit/05e9268dc28d209f9099ad2ea889b0b9b9f14cb9))
* **engine:** Remove obsolete docx mailmerge engine ([`698da36`](https://github.com/adfinis/document-merge-service/commit/698da3682b5657f3290ed274c4caf312c2e489f7))

### Fix

* **settings:** Make DOCXTEMPLATE_JINJA_EXTENSIONS setting optional ([`2ec2b63`](https://github.com/adfinis/document-merge-service/commit/2ec2b63b455792e4c586fc51f311f9cbc901d3f0))
* **deps:** Replace imghdr with python-magic ([`b6a4ca2`](https://github.com/adfinis/document-merge-service/commit/b6a4ca211a2aef19aefac7cc0bc4ce6998f86f0b))

### Breaking

* Remove dependency on MySQL. If you need to use mysql as a database, you may install the required dependency on top of the standard docker image. ([`08d909d`](https://github.com/adfinis/document-merge-service/commit/08d909db0adf7e32b0ed04fb4c00cc88c302be01))
* `document-merge-service` now uses Gunicorn as its app server instead of uWSGI. If you are using a custom uWSGI configuration via the `UWSGI_INI` env variable, replace it with a custom Gunicorn configuration as explained in [the documentation](CONFIGURATION.md#gunicorn). ([`aa3f24b`](https://github.com/adfinis/document-merge-service/commit/aa3f24b7f49c30a4b969ba83f89c522a4779929d))
* This will remove poetry entirely from the production image. If you customized the command, make sure to remove `poetry run` as the binaries are now globally available without using poetry. ([`73b9e43`](https://github.com/adfinis/document-merge-service/commit/73b9e4351636da53629acd4fe54eb9fba0c2855a))
* This fully removes the support of the docx mailmerge engine as the used library is quite inactive and there is no current use case for this engine. For more information, check issue #570. ([`698da36`](https://github.com/adfinis/document-merge-service/commit/698da3682b5657f3290ed274c4caf312c2e489f7))

## 7.3.7 (10 April 2025)

### Fix

* **ci:** Create container images also when pusblishing a draft release ([fb79d06](https://github.com/adfinis/document-merge-service/commit/fb79d06490661b06c66049b10d292b5ed92dcf55))

## 7.3.6 (8 April 2025)

### Fix

* **deps:** Fix locked dependency on django-storages ([`bf085a9`](https://github.com/adfinis/document-merge-service/commit/bf085a9808bdb76bb70bb8e834b92b6290384c73))
* **api:** Delete old file when updating template file ([`f98e38b`](https://github.com/adfinis/document-merge-service/commit/f98e38bdb1c1fff84e9e4f3c82d234250cd44c8d))

## 7.3.5 (13 January 2025)

### Fix

* **deps:** Update dependencies ([`16d4f76`](https://github.com/adfinis/document-merge-service/commit/16d4f767999989f46368f475e15a6335b5c06b28))

## 7.3.4 (12 December 2024)

### Fix

* **cache:** Cast common options for memcached cache ([`59f1727`](https://github.com/adfinis/document-merge-service/commit/59f1727b872f34da51757c894db5385170ff4fb4))

## 7.3.3 (10 December 2024)

### Fix

* **cache:** Add environment variable to configure cache options ([`6b45365`](https://github.com/adfinis/document-merge-service/commit/6b45365ac6cbc60b1739c75982f54934d57638bc))

## 7.3.2 (29 November 2024)

### Fix

* **deps:** Update dependencies ([`322e9ad`](https://github.com/adfinis/document-merge-service/commit/322e9ad7fb20c05198477f7c9c53598ca0c617e3))

## 7.3.1 (14 November 2024)

### Fix

* **merge:** Fix extension in filename when merging without convert ([`9676dab`](https://github.com/adfinis/document-merge-service/commit/9676dab2a859bfa3da4846d8e795bff09f870fbc))

## 7.3.0 (12 November 2024)

### Feature

* **api:** Accept available placeholders as json list ([`88887c4`](https://github.com/adfinis-sygroup/document-merge-service/commit/88887c464825301c04c7642a69977ed68bb6b512))

## 7.2.0 (11 October 2024)
### Feature
* **auth:** Make OIDC_USERNAME_CLAIM configurable ([`be82b1e`](https://github.com/luytena/document-merge-service/commit/be82b1ec20c4cc651c3cb61f0e48d71447a3a6c3))

### Fix
* **deps:** Update dependencies ([`4264f66`](https://github.com/luytena/document-merge-service/commit/4264f6657e2b56993a20b0ff1907a099094de03e))

## 7.1.1 (18 September 2024)
### Fix

* **sse-c:** Bump django-storages to include fix for head_object ([`b0a9601`](https://github.com/adfinis/document-merge-service/commit/b0a96015974f2f1fe0762b94b2459f10e3006ac8))

## 7.1.0 (18 September 2024)
### Fix

* **sse-c:** Bump django-storages to include fix for head_object ([`b0a9601`](https://github.com/adfinis/document-merge-service/commit/b0a96015974f2f1fe0762b94b2459f10e3006ac8))

## 7.1.0 (21 August 2024)
### Feature

* **template:** add new template model properties ([`1624693`](https://github.com/adfinis/document-merge-service/commit/16246933a821584ad5d88c65489a9849d8d4904b))

### Fix

* **template:** Only delete file if it exists ([`eef256a`](https://github.com/adfinis/document-merge-service/commit/eef255add8a5fff5705ba9ce063acc7b09beef03))
* **template:** Raise the maximum number of fields for the data upload ([`bbbb82b`](https://github.com/adfinis/document-merge-service/commit/bbbb82ba805a2741ddf9364c697713e31b644ce2))

## 7.0.2 (9 August 2024)
### Fix

* **deps:** Update django ([`4f0cee5`](https://github.com/adfinis/document-merge-service/commit/4f0cee592bd5636c696281df0ff1471ea734c09f))

## 7.0.1 (19 July 2024)
### Fix

* Ssec download ([`d6e043d`](https://github.com/adfinis/document-merge-service/commit/d6e043d93203c0edcbae7962b1008717dcae9f08))

## 7.0.0 (17 July 2024)
### Feature

* **s3:** Add s3 ssec option ([`7829a2c`](https://github.com/adfinis/document-merge-service/commit/7829a2cba627eedc7f3c97bca666973f387e61d6))

### Breaking

* prefix storage env vars with dms for django-storages to avoid conflicts ([`8fc5649`](https://github.com/adfinis/document-merge-service/commit/8fc564985d9516a71a5acdd9651134ec5add2a86))
* removed support for python 3.8 and 3.9 ([`8ef1733`](https://github.com/adfinis/document-merge-service/commit/8ef1733ed279594ab415d1a53f2fa926bebfc758))

## 6.6.1 (1 July 2024)
### Chore

This is a pure maintenance release. Most noteworthy commit is:

* chore: replace unmaintained docx-mailmerge with docx-mailmerge2 ([`57fcd23`](https://github.com/adfinis/document-merge-service/commit/57fcd230b08557f43128b8df70e23caa629494fb))

## 6.6.0 (18 June 2024)
### Feature

* **image:** Allow images to keep their original aspect ratio ([`05ade2b`](https://github.com/adfinis/document-merge-service/commit/05ade2b41f6668d7c92fb9fde9951977a8972753))

## 6.5.2 (12 June 2024)
### Fix

* Use a sandboxed environment ([#763](https://github.com/adfinis/document-merge-service/issues/763)) ([`a1edd39`](https://github.com/adfinis/document-merge-service/commit/a1edd39d33d1bdf75c31ea01c317547be90ca074))

## 6.5.1 (3 June 2024)
### Fix

* **deps:** Allow caching with memcache ([`2f7c2bc`](https://github.com/adfinis/document-merge-service/commit/2f7c2bc196f56dd5488101c8ad1e639671002005))
* **deps:** Fix usage with postgres database ([`f29c763`](https://github.com/adfinis/document-merge-service/commit/f29c7635d3fa7759c9c9e98bc6e437da650ebb26))

## 6.5.0 (30 May 2024)
### Feature

* **docker:** Update python to v3.12 ([`14c4d7f`](https://github.com/adfinis/document-merge-service/commit/14c4d7f97005ce9651be6dc37eae904125614e29))
* **deps:** Update dependencies ([`5773d5c`](https://github.com/adfinis/document-merge-service/commit/5773d5c5283543c843c4986daf8b71cc1cafa611))
* **deps:** Update django to v4.2 LTS ([`5287a3e`](https://github.com/adfinis/document-merge-service/commit/5287a3e4a6b26c12e122026f789e80d2c70f892b))

### Fix

* **docker:** Install dependencies as dms user ([`6a17a8f`](https://github.com/adfinis/document-merge-service/commit/6a17a8f1cfce053440790e9b62a7d6c21405f580))

## 6.4.6 (12 June 2024) (Backport)
### Fix

* Use a sandboxed environment ([#763](https://github.com/adfinis/document-merge-service/issues/763)) ([`a1edd39`](https://github.com/adfinis/document-merge-service/commit/a1edd39d33d1bdf75c31ea01c317547be90ca074))

## 6.4.5 (25 April 2024)
### Fix
* **image:** Fix template validation with images in headers / footers ([`eccbb34`](https://github.com/adfinis/document-merge-service/commit/eccbb34ce69cd26a998a8ef15db109e8faf2a1e3))

## 6.4.4 (24 January 2024)
### Fix
* **settings:** Add s3 ssl settings ([#698](https://github.com/adfinis/document-merge-service/issues/698)) ([`c92b381`](https://github.com/adfinis/document-merge-service/commit/c92b381ce6ebc45c0b96eba828b471f2bd28a169))


## 6.4.3 (23 October 2023)
### Fix
* **convert:** Handle file names with multiple dots ([`3ae90f1`](https://github.com/adfinis/document-merge-service/commit/3ae90f1d3e8e2bfce86528be2af142975b6f1a58))

## 6.4.2 (25 September 2023)
### Fix

* **deps:** Downgrade urllib to v1 ([`d7ab8ce`](https://github.com/adfinis/document-merge-service/commit/d7ab8ce0159b61d0c661953735bfed5ead370605))

## 6.4.1 (09 August 2023)
### Fix

* Improve command to upload local template files to storage backend ([`4589dcb`](https://github.com/adfinis/document-merge-service/commit/4589dcba025f82ffc23726f7284856755268ab10))

## 6.4.0 (03 August 2023)
### Feature
* Allow conversion of docx and odt files to pdf using a new convert endpoint ([`e00e49e`](https://github.com/adfinis/document-merge-service/commit/e00e49e210b17469457b76eccf306f17b40da43a))

## 6.3.1 (31 July 2023)
### Fix

* **auth:** Don't run any authentication logic if auth is disabled ([`564b504`](https://github.com/adfinis/document-merge-service/commit/564b504be673f34677eb6736a3b26dbbfdd3d7ec))

## 6.3.0 (25 July 2023)
### Feature

* **extensions:** Add setting for passing custom arguments into extensions ([`b76e293`](https://github.com/adfinis/document-merge-service/commit/b76e2930535f15820e449930e57d004c54e1ba2d))

## 6.2.2 (24 July 2023)
### Fix

* **template:** Migrate group to meta property before removing ([`4480877`](https://github.com/adfinis/document-merge-service/commit/448087728f3103744b8245ff5400b63201352b19))

## 6.2.1 (19 July 2023)
### Fix

* **dgap:** Add env variables to configure permissions and visibilities ([`67fc95a`](https://github.com/adfinis/document-merge-service/commit/67fc95a16f72e7afed37342972c6101c492d529a))
* Storage generic file cleanup ([`0633fd2`](https://github.com/adfinis/document-merge-service/commit/0633fd20a7a11f00a8d7eb6aa903aa38520fe8b1))

## 6.2.0 (11 July 2023)
### Feature
* Add django storages and settings for s3 storage ([`6df1a83`](https://github.com/Yelinz/document-merge-service/commit/6df1a83a4befbb8687a951d45fe6910deba83272))

## 6.1.2 (10 May 2023)
Maintenance release only containing dependency updates.

## 6.1.1 (03 May 2023)
### Fix
* **excel:** Set `sheet_name` and `tpl_name` to load the correct sheet
([`13a2a07`](https://github.com/adfinis/document-merge-service/commit/13a2a073aa1a7f65cbf7c794210f460db1a2509e))

## 6.1.0 (27 January 2023)
### Feature
* **filters:** Add template meta filter ([`2daf8ec`](https://github.com/Yelinz/document-merge-service/commit/2daf8ec736a9ff5ee424548ef9eef53362e284e0))
* Add sentry integration ([`abe37f1`](https://github.com/Yelinz/document-merge-service/commit/abe37f1417554119299acb8aa852892bae823490))

### Fix
* **auth:** Add userinfo to authenticated user ([`21ae809`](https://github.com/Yelinz/document-merge-service/commit/21ae809dd6e08d1b5823373637ef17805640d73a))
## 6.0.0 (12 January 2023)
### Feature
* Add dgap mixins ([`1b9f486`](https://github.com/Yelinz/document-merge-service/commit/1b9f486db20fc8856086f91e22e92801fb4b5079))

### Fix
* Remove oidc group api fetching ([`e64e9d5`](https://github.com/Yelinz/document-merge-service/commit/e64e9d5c563f8ab961b5d35aa87d280c1d6a39ca))
* **api:** Fix install failing without mysql ([`b984054`](https://github.com/Yelinz/document-merge-service/commit/b9840542058f06895bdcfa19559a115bef9dedb6))
* **settings:** Enable email settings without email error handler ([`e12480d`](https://github.com/Yelinz/document-merge-service/commit/e12480d58b00e4aa7409ff9c8f68bf6b4cec31d9))

### Breaking
* remove oidc group api fetching ([`e64e9d5`](https://github.com/Yelinz/document-merge-service/commit/e64e9d5c563f8ab961b5d35aa87d280c1d6a39ca))
* add dgap mixins ([`1b9f486`](https://github.com/Yelinz/document-merge-service/commit/1b9f486db20fc8856086f91e22e92801fb4b5079))

## 5.2.1 (6 January 2023)

### Fix
* Fix wrong env variable for server email address ([`d1006b9`](https://github.com/adfinis/document-merge-service/commit/d1006b9f9aaf74d15d076e4a0856416f3ff9e6aa))

## 5.2.0 (6 January 2023)

### Feature
* Add email error handler ([`012a893`](https://github.com/adfinis/document-merge-service/commit/012a893eb5b17b5f90899035d292a005fe118279))

## 5.1.0 (4 October 2022)

### Feature
* **api:** Make pagination configurable ([`dd6615f`](https://github.com/adfinis/document-merge-service/commit/dd6615f14b81ec005b697bf43c58d3c74e8d3fe3))

## 5.0.6 (13 September 2022)

### Fix
* Also log unshare in formats-call / only test unshare in error-path ([`dd0f22c`](https://github.com/adfinis-sygroup/document-merge-service/commit/dd0f22c0e97139e9f5559da70683d20a6927fb5d))

## 5.0.5 (01 September 2022)

### Fix
* **validation:** Fix excel template validation ([`3c6149e`](https://github.com/adfinis-sygroup/document-merge-service/commit/3c6149e15a455539f544c61084a0e372cc74fa7b))

## 5.0.4 (29 August 2022)

### Fix
* Allow isolation of unoconv calls to be disabled (default) ([`74834f1`](https://github.com/adfinis-sygroup/document-merge-service/commit/74834f1c820eb258e53697ecd563f1ee353a5e66))
* Remove security restrictions to make unshare possible ([`5b10cff`](https://github.com/adfinis-sygroup/document-merge-service/commit/5b10cffac5bd365d02c16999748113747d6d36e9))

## 5.0.3 (23 August 2022)

Important: Be aware that the docker-container needs CAP_SYS_ADMIN since version 4.7.0

### Fix
* Log an error if unoconv or unshare fails ([`6e2f54a`](https://github.com/adfinis-sygroup/document-merge-service/commit/6e2f54ad961cdfb0052c0a03823121ccf53b68ae))

## 5.0.2 (22 August 2022)

### Fix
* Move temporary path to data directory
([`afce2ca`](https://github.com/adfinis-sygroup/document-merge-service/commit/afce2ca3429bf20d6c282fe5f8a1f1201fc278ee))

## 5.0.1 (9 August 2022)

### Fix
* **docker:** Fix docker uwsgi command ([`85892f6`](https://github.com/adfinis/document-merge-service/commit/85892f63005fe31b277ba8df623c8a0ec0f1b7ec))

## 5.0.0 (9 August 2022)

### Feature
* **license:** Switch license from MIT to GPL-3.0-or-later ([`47c1a84`](https://github.com/adfinis/document-merge-service/commit/47c1a843a9cda105d1640651a8231fbc4c18039f))

### Fix
* **python:** Use python v3.8 ([`920c0bd`](https://github.com/adfinis/document-merge-service/commit/920c0bd2c5c0dfe836b5b215a91691a4077fd63b))

### Breaking
* Drop support for Python v3.7. This should have been done in 29a49ee76b638f0a8fb7b189fb91e61c45d78bde which updated the python version to 3.10 which is too restrictive. We now guarantee support for python versions 3.7 to 3.10.  ([`920c0bd`](https://github.com/adfinis/document-merge-service/commit/920c0bd2c5c0dfe836b5b215a91691a4077fd63b))
* document-merge-service is now released under the GPL-3.0-or-later license.  ([`47c1a84`](https://github.com/adfinis/document-merge-service/commit/47c1a843a9cda105d1640651a8231fbc4c18039f))

## 4.7.0 (26 July 2022)

### Feature
* Isolate libreoffice instances ([`9e2db65`](https://github.com/adfinis/document-merge-service/commit/9e2db651a9804c787e7909baa415aa36e551007b))
* **engines:** Add basic excel validation ([`f396ae8`](https://github.com/adfinis/document-merge-service/commit/f396ae8879475d6c4aca29003f77965945da24fd))
* **engines:** Render all excel-sheets with thee same data ([`ca54651`](https://github.com/adfinis/document-merge-service/commit/ca54651ac85c5576fac5162ba1caaebff273f87b))
* **engines:** Test datastructures with excel templates ([`9a5c116`](https://github.com/adfinis/document-merge-service/commit/9a5c116c30c22957c9ee316c0c0f4baa9c3dba98))
* **engines:** Create template test ([`8c4cad1`](https://github.com/adfinis/document-merge-service/commit/8c4cad1273f35496080473f42ecb150a575b0a2e))
* **engines:** Fix code for new xlsx library ([`ca4a6a4`](https://github.com/adfinis/document-merge-service/commit/ca4a6a42dfb58196e7a819e1c9b2a4cd9b59dbe8))
* **engines:** Add xlsx template engine ([`e133c83`](https://github.com/adfinis/document-merge-service/commit/e133c834128916eb26ff7642e6eb31852406743c))

### Fix
* Cleanup thread pool ([`fec982e`](https://github.com/adfinis/document-merge-service/commit/fec982e25209b1088477f868bfa786f087d047bc))

## 4.6.2 (21 January 2022)

### Fix
* **cleanup:** Convert cleanup migration to command ([#467](https://github.com/adfinis/document-merge-service/issues/467)) ([`33052ee`](https://github.com/adfinis/document-merge-service/commit/33052eed48dc01a311aa57462d3a64595b74e743))
* **cleanup-migration:** Fail gracefully in new container ([`8a93339`](https://github.com/adfinis/document-merge-service/commit/8a93339be1218fe79579129483f238f17e67d2e9))

## 4.6.1

### Fix
* **api:** Do not crash in list view ([#458](https://github.com/adfinis/document-merge-service/issues/458)) ([`11b02fd`](https://github.com/adfinis/document-merge-service/commit/11b02fd58a6a0d38d10bb6a67da9999e11f0c07f))

## 4.6.0

### Feature
* Add config for deployment under specific URL prefix ([#456](https://github.com/adfinis/document-merge-service/issues/456)) ([`6801024`](https://github.com/adfinis/document-merge-service/commit/680102457b938b33b2ecbc314bcb1897644c519a))

### Fix
* **template:** Make template download url more stable ([`3438a53`](https://github.com/adfinis/document-merge-service/commit/3438a53efbd7bbe46cf3b38659e1bebc4cfe348b))
* **cleanup:** Delete old files when template is deleted or changed ([#445](https://github.com/adfinis/document-merge-service/issues/445)) ([`26c9570`](https://github.com/adfinis/document-merge-service/commit/26c9570e02dcc981ee523273a06137caa9bf8486))
* **jinja:** Autoescape data passed to template when merging ([#444](https://github.com/adfinis/document-merge-service/issues/444)) ([`2ac030e`](https://github.com/adfinis/document-merge-service/commit/2ac030e619899a55bc72440f55081258e1ab66ac))

### Documentation
* **readme:** Remove deprecated dependabot badge ([`4173a3b`](https://github.com/adfinis/document-merge-service/commit/4173a3bf6d26d02afd05fc3972492054e3476f5f))


## 4.5.0

### Feature
* Add meta-field to Template ([`27163e8`](https://github.com/adfinis/document-merge-service/commit/27163e8c5b2d1541566e4908ac88e55a3d5bc7b9))

### Fix
* Reduce number of uwsgi processes ([`46f950a`](https://github.com/adfinis/document-merge-service/commit/46f950a7a5ff6ca99c20941a5d1ec0a7cbd1bde0))
* Add uwsgi config suitable for production use ([`247c5df`](https://github.com/adfinis/document-merge-service/commit/247c5dfbc9e00e29a95b21f2646ad735368cdc21))
* **jinja:** Replace deprecated contextfilter with pass_context ([`3308cd1`](https://github.com/adfinis/document-merge-service/commit/3308cd11aac3332445053b1d9ac4564bb7034a06))

## 4.4.0

### Feature
* run subprocesses with timeout and cleanup forks
([`be092b4`](https://github.com/adfinis/document-merge-service/commit/be092b464d0120ce1d6e9bc8afdf4150cacd2710))

## 4.3.0

### Feature
* Allow disabling validation
([`f371b33`](https://github.com/adfinis/document-merge-service/commit/f371b339d7434b01b2a024308fc58f0806d8a287))

## 4.2.1

### Fix
* Fix using same image multiple times in template (35b7ffb9cff7e4577f505823449874361d1557a2)

## 4.2.0

### Feature
* Handle None for images (fd6f55d61e1877e0203d7ee4212641816119077c)

### Fix
* Dont crash when accessing undefined value in template (f2bb378dbb51a61d3d4e1f01afcf2b3efd831aba)


## 4.1.0
### Feature
* Support inline images for docx-template (37e42724c75a5f5c8ab60ee45a2fd64118cdf407)

### Fix
* Correctly validate image placeholders (9617bd71db90901ae0e18c513bc28bb3225b7857)
* Also add template to context in engine validation (639e9c27435873ca8680308684d799ea9da29d6a)


## 4.0.1

### Fix
* Don't reject templates with complex syntax (fb56a42aee82f9261596f7546f52f8b9930292de)


## 4.0.0

### Breaking
* Remove support for external unoconv listeners
  * `UNOCONV_SERVER` and `UNOCONV_PORT` are no longer supported configuration options. Please remove
	them from your configuration file.
  * By default an unoconv process gets launched within the container.

### Feature
* Check template for available placeholders (2ac9aeb95016665520bef53c7e3ac0310be9f84f)
* Allow to validate docx template on upload (de810446fbec2ffe610cda4f9cb12be34b5bdbb5)

### Fix
* Make sure port is always printed as string (dd8f34b93a9f3b279fa8e99b1b8ba3d8e1d582fb)

### Documentation
* Extended user guide (09f0393ec7fe40513fcd47473272a09cf0a294d3)


## 3.0.0

### Fix
* Revert automatic conversion, add filter instead (4e91c50a5938ab641a90cb84fabd56ff992c757c)

### Breaking
* Replace tfk-api-unoconv service with unoconv listener (f12f0a221b64fb22665ac4609e4f52e34ff767f2)
  * `UNOCONV_LOCAL` and `UNOCONV_URL` are no longer supported configuration options. Please remove
	them from your configuration file.
  * By default an unoconv listener gets launched within the container. To use a different listener
	you can specify `UNOCONV_SERVER` and `UNOCONV_PORT`.

* After gathering some practical experience with the new automatic "Listing"-conversion for
  multiline we noticed that this feature is a little bit too "clever" and breaks many advanced
  use-cases. (4e91c50a5938ab641a90cb84fabd56ff992c757c)
