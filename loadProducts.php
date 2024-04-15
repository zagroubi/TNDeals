<?php


$dsn = "mysql:host=localhost;port=3306;dbname=TNDeals;charset=utf8mb4";
$username = "root";
$password =  [REDACTED];


$category = $_GET['category'] ? urldecode($_GET['category']) : '';
$searchKeyword = $_GET['keyword'] ? urldecode($_GET['keyword']): '';
$page = isset($_GET['page']) ? intval($_GET['page']) : 1;
$suppliers = $_GET['suppliers'] ? urldecode($_GET['suppliers']) : '';


$perPage = 10;
$offset = ($page - 1) * $perPage; 


# Prevent SQL injection in category
$validCategories = array("laptops", "phones", "desktops", "accessories", "monitors", "consoles", "components");
if (!in_array($category, $validCategories)) {
    $category = "laptops";
}

try {
    $pdo = new PDO($dsn, $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    

    if ($searchKeyword == '' && $suppliers == '') {
        $statement = $pdo->prepare("SELECT * FROM $category LIMIT :perPage OFFSET :offset");

        // pagination
        $statement2 = $pdo->prepare("SELECT COUNT(*) FROM $category");
    }
    else if($searchKeyword == '' && $suppliers != ''){
        $supps = explode(",", $suppliers);
        $supps = "'" . implode("','", $supps) . "'";

        $statement = $pdo->prepare("SELECT * FROM $category WHERE supplier IN ($supps) LIMIT :perPage OFFSET :offset");

        // pagination
        $statement2 = $pdo->prepare("SELECT COUNT(*) FROM $category WHERE supplier IN ($supps)");
        
        
    } 
    else if ($searchKeyword != '' && $suppliers == '') {
        $statement = $pdo->prepare("SELECT * FROM $category WHERE title LIKE :keyword OR description LIKE :keyword LIMIT :perPage OFFSET :offset");
        $statement->bindValue(':keyword', '%' . $searchKeyword . '%', PDO::PARAM_STR);

        // pagination
        $statement2 = $pdo->prepare("SELECT COUNT(*) FROM $category WHERE title LIKE :keyword OR description LIKE :keyword");
        $statement2->bindValue(':keyword', '%' . $searchKeyword . '%', PDO::PARAM_STR);
    }
    else if ($searchKeyword != '' && $suppliers != ''){

        $supps = explode(",", $suppliers);
        $supps = "'" . implode("','", $supps) . "'";

        $statement = $pdo->prepare("SELECT * FROM $category WHERE (title LIKE :keyword OR description LIKE :keyword) AND supplier IN ($supps) LIMIT :perPage OFFSET :offset");
        $statement->bindValue(':keyword', '%' . $searchKeyword . '%', PDO::PARAM_STR);

        // pagination
        $statement2 = $pdo->prepare("SELECT COUNT(*) FROM $category WHERE (title LIKE :keyword OR description LIKE :keyword) AND supplier IN ($supps)");
        $statement2->bindValue(':keyword', '%' . $searchKeyword . '%', PDO::PARAM_STR); 

    }

    $statement->bindValue(':perPage', $perPage, PDO::PARAM_INT);
    $statement->bindValue(':offset', $offset, PDO::PARAM_INT);
    $statement->execute();

    $products = $statement->fetchAll(PDO::FETCH_ASSOC);

    //pagination
    $statement2->execute();
    $totalProducts = $statement2->fetchColumn();
    $totalPages = ceil($totalProducts / $perPage);

    if (count($products)>0){

        echo "<div class='pagination'>";
        for ($i = 1; $i <= $totalPages; $i++) {
            $activeClass = ($i == $page) ? "active" : "";
            echo "<button class='number $activeClass' onclick='changePage(\"$category\",\"$searchKeyword\",$i,\"$suppliers\")'>$i</button>";
        }
        echo "</div>";


        foreach ($products as $product) {
            $value = $product['discount_amount'];
            $cleaned_value = str_replace(',', '.', $value);
            $cleaned_value = preg_replace('/[^0-9.]/', '', $cleaned_value);
            $number = (float) $cleaned_value;

            if ($number<=100){
                $amount = "low";
            }else if ($number>100 && $number<=200){
                $amount = "medium";
            }else{
                $amount = "high";
            }
            
            echo "
            <div class='card {$amount}'>
                <img src='{$product['image']}' alt='Product Image'>
                <div class='card-content'>
                    <p>{$product['title']}</p>
                    <hr>
                    <p>{$product['description']}</p>
                    <div id='prices'>
                        <p>{$product['before_discount']}</p>
                        <p>{$product['after_discount']}</p>
                        <p>| -$number DT</p>
                    </div>
                    <hr>
                    <p>Supplier: <b>{$product['supplier']}</b></p>
                    <p>Link: <a href='{$product['url']}' target=_blank>{$product['url']}</a></p>
                </div>
                
            </div>";
        }

    
    }else {
        echo "<h1 style='color:#333;text-align:center;font-size:40px;'>" . "Sorry, No Items Found :(" . "</h1>";
    }

} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
