from bs4 import BeautifulSoup

# Example HTML content (replace this with your actual HTML)
html_content = """
                    </div>
                </div>
                <div class="ammenu-robots-navigation">
                    <nav class="navigation" data-action="navigation" aria-disabled="true" aria-hidden="true"
                        tabindex="-1">
                        <ul aria-disabled="true" aria-hidden="true">
                            <li class="category-item&#x20;nav-0" role="presentation"><a
                                    href="https://extranet.martinex.se/hemma" tabindex="-1" title="Hemma">Hemma</a>
                                <ul class="submenu">
                                    <li class="category-item&#x20;nav-0-0" role="presentation"><a
                                            href="https://extranet.martinex.se/hemma/duka" tabindex="-1"
                                            title="Duka">Duka</a>
                                        <ul class="submenu">
                                            <li class="category-item&#x20;nav-0-0-0" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/muggar" tabindex="-1"
                                                    title="Muggar">Muggar</a> </li>
                                            <li class="category-item&#x20;nav-0-0-1" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/tallrikar"
                                                    tabindex="-1" title="Tallrikar">Tallrikar</a> </li>
                                            <li class="category-item&#x20;nav-0-0-2" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/skalar" tabindex="-1"
                                                    title="Sk&#xE5;lar">Skålar</a> </li>
                                            <li class="category-item&#x20;nav-0-0-3" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/serveringskarl"
                                                    tabindex="-1" title="Serveringsk&#xE4;rl">Serveringskärl</a> </li>
                                            <li class="category-item&#x20;nav-0-0-4" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/drickflaskor"
                                                    tabindex="-1" title="Drickflaskor">Drickflaskor</a> </li>
                                            <li class="category-item&#x20;nav-0-0-5" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/barnserviser"
                                                    tabindex="-1" title="Barnserviser">Barnserviser</a> </li>
                                            <li class="category-item&#x20;nav-0-0-6" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/duka/ovrigt" tabindex="-1"
                                                    title="&#xD6;vrigt">Övrigt</a> </li>
                                        </ul>
                                    </li>
                                    <li class="category-item&#x20;nav-0-1" role="presentation"><a
                                            href="https://extranet.martinex.se/hemma/kok" tabindex="-1"
                                            title="K&#xF6;k">Kök</a>
                                        <ul class="submenu">
                                            <li class="category-item&#x20;nav-0-1-0" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/kok/ugnsformar"
                                                    tabindex="-1" title="Ugnsformar">Ugnsformar</a> </li>
                                            <li class="category-item&#x20;nav-0-1-1" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/kok/matlagning"
                                                    tabindex="-1" title="Matlagning">Matlagning</a> </li>
                                            <li class="category-item&#x20;nav-0-1-2" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/kok/koksredskap"
                                                    tabindex="-1" title="K&#xF6;ksredskap">Köksredskap</a> </li>
                                            <li class="category-item&#x20;nav-0-1-3" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/kok/baksredskap"
                                                    tabindex="-1" title="Bakredskap">Bakredskap</a> </li>
                                            <li class="category-item&#x20;nav-0-1-4" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/kok/kakmatt" tabindex="-1"
                                                    title="Kakm&#xE5;tt">Kakmått</a> </li>
                                        </ul>
                                    </li>
                                    <li class="category-item&#x20;nav-0-2" role="presentation"><a
                                            href="https://extranet.martinex.se/hemma/inreda" tabindex="-1"
                                            title="Inreda">Inreda</a>
                                        <ul class="submenu">
                                            <li class="category-item&#x20;nav-0-2-0" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/inreda/prydnader"
                                                    tabindex="-1" title="Prydnader">Prydnader</a> </li>
                                            <li class="category-item&#x20;nav-0-2-1" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/inreda/bruksforemal"
                                                    tabindex="-1" title="Bruksf&#xF6;rem&#xE5;l">Bruksföremål</a> </li>
                                        </ul>
                                    </li>
                                    <li class="category-item&#x20;nav-0-3" role="presentation"><a
                                            href="https://extranet.martinex.se/hemma/forvara" tabindex="-1"
                                            title="F&#xF6;rvara">Förvara</a>
                                        <ul class="submenu">
                                            <li class="category-item&#x20;nav-0-3-0" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/forvara/platburkar"
                                                    tabindex="-1" title="Pl&#xE5;tburkar">Plåtburkar</a> </li>
                                            <li class="category-item&#x20;nav-0-3-1" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/forvara/ovriga-burkar"
                                                    tabindex="-1" title="&#xD6;vriga&#x20;burkar">Övriga burkar</a>
                                            </li>
                                        </ul>
                                    </li>
                                    <li class="category-item&#x20;nav-0-4" role="presentation"><a
                                            href="https://extranet.martinex.se/hemma/hemtextiler" tabindex="-1"
                                            title="Hemtextiler">Hemtextiler</a>
                                        <ul class="submenu">
                                            <li class="category-item&#x20;nav-0-4-0" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/hemtextiler/sangklader"
                                                    tabindex="-1" title="S&#xE4;ngkl&#xE4;der">Sängkläder</a> </li>
                                            <li class="category-item&#x20;nav-0-4-1" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/hemtextiler/handdukar"
                                                    tabindex="-1" title="Handdukar">Handdukar</a> </li>
                                            <li class="category-item&#x20;nav-0-4-2" role="presentation"><a
                                                    href="https://extranet.martinex.se/hemma/hemtextiler/kokstextilier"
                                                    tabindex="-1" title="K&#x3F;&#x3F;kstextilier">K??kstextilier</a>
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                            </li>
"""


def extract_links(html_content):
    """Extract links for specific overcategories and their subcategories."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Overcategories to sort and extract
    overcategories = {
        "Duka": [],
        "Kök": [],
        "Inreda": [],
        "Förvara": [],
        "Hemtextiler": []
    }

    # Find all overcategories
    categories = soup.select("li.category-item > a")
    for category in categories:
        title = category.get("title", "").strip()
        href = category.get("href", "").strip()

        # Check if the title matches one of the overcategories
        if title in overcategories:
            overcategories[title].append(href)

            # Find subcategories within this overcategory
            submenu = category.find_next("ul", class_="submenu")
            if submenu:
                subcategory_links = submenu.select("a")
                for sub_link in subcategory_links:
                    sub_href = sub_link.get("href", "").strip()
                    if sub_href:
                        overcategories[title].append(sub_href)

    return overcategories


# Extract and print the links
sorted_links = extract_links(html_content)

for category, links in sorted_links.items():
    print(f"{category} ({len(links)} links):")
    for link in links:
        print(link)
    print()
