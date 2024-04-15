

<header>
    <ul id="nav">
        <li><a  id='load'href="?#laptops" onclick="loadProducts('laptops')">Laptops</a></li>
        <li><a href="?#desktops" onclick="loadProducts('desktops')">Desktops</a></li>
        <li><a href="?#monitors" onclick="loadProducts('monitors')">Monitors</a></li>
        <li><a href="?#phones" onclick="loadProducts('phones')">Phones</a></li>
        <li><a href="?#components" onclick="loadProducts('components')">Components</a></li>
        <li><a href="?#consoles" onclick="loadProducts('consoles')">Consoles</a></li>
        <li><a href="?#accessories" onclick="loadProducts('accessories')">Accessories</a></li>
    </ul>
    <div class="search-box">
        <form onsubmit="searchProducts(window.location.hash);">
            <input type="text" id="search-input" class="search-input" placeholder="Enter Keyword">
            <button type="submit" class="search-button">Search</button>
        </form>
    </div>
</header>