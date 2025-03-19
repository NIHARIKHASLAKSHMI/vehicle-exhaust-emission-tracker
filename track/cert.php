<?php
include("dbconnect.php");
extract($_REQUEST);

$q1=mysqli_query($connect,"SELECT * FROM ve_register where uname='$vid'");
$r1=mysqli_fetch_array($q1);

$xid=$vid.".jpg";
///////////////text/////
$image = imagecreatefromjpeg('img/cert1.jpg');
$vno=$r1['vno'];
$vtype=$r1['vtype'];
$vname=$r1['vname'];
$vmodel=$r1['vmodel'];
$fuel=$r1['fuel_type'];

$fontSize = 12;
$fontColor = imagecolorallocate($image, 0, 0, 0); //  color

// Define the coordinates where the text will be placed (top-left corner)
$textX = 20;
$textY = 40;

// Add the text to the image
imagettftext($image, $fontSize, 0, 188,216, $fontColor, 'arial.ttf', $vno);
imagettftext($image, $fontSize, 0, 188,296, $fontColor, 'arial.ttf', $vtype);
imagettftext($image, $fontSize, 0, 188,328, $fontColor, 'arial.ttf', $vname);
imagettftext($image, $fontSize, 0, 188, 354, $fontColor, 'arial.ttf', $vmodel);
imagettftext($image, $fontSize, 0, 543, 356, $fontColor, 'arial.ttf', $fuel);

// Output or save the final image
imagejpeg($image, 'upload/'.$xid);



?>
