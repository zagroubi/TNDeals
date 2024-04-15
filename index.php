<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>TNDeals</title>

</head>
<body>
    <?php require('partials/header.php') ?>
    
    <main id="main">
        <?php require('partials/filter.php') ?>

        <div id="container"></div>

        <div id="back-to-top" onclick="scrollToTop()"> ▲ </div>
    </main>

    <?php require('partials/footer.php') ?>

    <script src="main.js"></script>
    <script src="scrollUp.js"></script>
</body>
</html>
