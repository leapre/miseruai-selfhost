import requests, xml.etree.ElementTree as ET

SITEMAP_URL = "https://miyablog.info/sitemap.xml"

def get_urls_from_sitemap(url: str) -> list[str]:
    xml_text = requests.get(url, timeout=10).text
    root = ET.fromstring(xml_text)
    # <urlset> 直下の <loc> を全部拾う
    urls = [loc.text for loc in root.iterfind(".//{*}loc")]
    return urls

if __name__ == "__main__":
    urls = get_urls_from_sitemap(SITEMAP_URL)
    print(f"{len(urls)} URLs found")
    # 後続で trafilatura 抽出に回す