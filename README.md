# tplink-grab
Downloads all GPL tarballs from TP-Link by parsing `https://www.tp-link.com/au/choose-your-location/`, then extracting country-specific `support/gpl-code/` pages to get lists of tarballs
The pages are structured in such a way that they'll either have direct links to `tar.gz` files or similar, or Javascript generates links to a page like `https://www.tp-link.com/phppage/gpl-res-list.html?model=Deco%20M5&appPath=kz` for each model and country code