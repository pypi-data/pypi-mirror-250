
import vitamin_c_crawler as vc_crawler
import config  # Ensure this script also has access to config

if __name__ == '__main__':
    vc_crawler.crawl_vitamin_c_products(
        time_limit=config.TIME_LIMIT,
        source=config.SOURCE_URL,
        download_images=config.DOWNLOAD_IMAGES
    )
