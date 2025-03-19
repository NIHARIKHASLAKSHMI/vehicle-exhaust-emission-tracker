<?php
include("dbconnect.php");



?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Untitled Document</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$(document).ready(function(){
    // Function to reload specific content via AJAX
    function reloadContent() {
        $.ajax({
            url: 'track2.php', // URL to fetch updated content
            type: 'GET',
            success: function(data) {
                // Create a new element with the updated content
                var $newContent = $('<div>').html(data);
                // Replace the existing content with the new content
                $('#contentToUpdate').replaceWith($newContent);
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    }

    // Reload content every 10 seconds
    setInterval(reloadContent, 10000);
});
</script>
</head>

<body>
<div id="contentToUpdate">
<?php

$fp=fopen("det.txt","r");
$det=@fread($fp,filesize("det.txt"));
	if($det!="")
	{
$vv=explode(",",$det);
?>
<table border="0" width="60%">

<?php
foreach($vv as $v1)
{
	$v11=explode("|",$v1);
	$v2=$v11[0];
$q3=mysqli_query($connect,"select * from ve_register where id=$v2");
	$r3=mysqli_fetch_array($q3);
?>
<tr>
<td style="background-color:#000066; color:#FFFFFF; line-height:25px"><?php echo $r3['name']; ?> [Vehicle No: <?php echo $r3['vno']; ?>]</td>
</tr>
<tr>
<?php
	
	?>
	<td>
	Vehicle: <?php echo $r3['vname']." ".$r3['vmodel']." (".$r3['vtype'].")"; ?><br />
	Fuel Type: <?php echo $r3['fuel_type']; ?>
	
	</td>
	<?php
?>
</tr>
<tr>
<td style="border-bottom:dotted 1px #003366">&nbsp;</td>
</tr>
<?php	
}
?>
</table>
	<?php
	}
	?>
</div>
</body>
</html>
