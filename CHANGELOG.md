# Changelog

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
