<?php
include("dbconnect.php");

$rdate=date("d-m-Y");
$ch1=mktime(date('H')+5,date('i')+30,date('s'));
$rtime=date('H:i:s',$ch1);

$qrt=mysqli_query($connect,"SELECT * FROM ve_rto order by id desc");
$rrt=mysqli_fetch_array($qrt);
$mobile2=$rrt['mobile'];
?>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Untitled Document</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="../../static/web/css/style.css" rel="stylesheet">
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$(document).ready(function(){
    // Function to reload specific content via AJAX
    function reloadContent() {
        $.ajax({
            url: 'track1.php', // URL to fetch updated content
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
<style type="text/css">
.box {
    height: 402px;
    width: 947px;
	overflow:hidden;
	padding-left:20px;
    -ms-transform: rotate(-8deg); /* IE 9 */
    -webkit-transform: rotate(-8deg); /* Safari */
    transform: rotate(-8deg); /* Standard syntax */
?   
}
</style>
</head>

<body>
<div id="contentToUpdate">
<?php
$q1=mysqli_query($connect,"SELECT * FROM ve_register where ban_st=0 && service_st=0 order by rand()");
$cnt=mysqli_num_rows($q1);
   
$data=array();
$val=array();
$rn=rand(1,$cnt);
    
    $i=1;
    
    while($r1=mysqli_fetch_array($q1))
	{
        
        if($i<=$rn)
		{
		$rid=$r1['id'];
            $q2=mysqli_query($connect,"SELECT * FROM ve_register where id=$rid");
            $r2=mysqli_fetch_array($q2);

            $vt=$r2['vtype'];
            $vv="";
            if($vt=="Car")
			{
                $rn2=rand(1,3);
                $vv="c".$rn2.".png";
            }
			else
			{
                if($vt=="Bus")
				{
                    $vv="c5.png";
				}
                else if($vt=="Van")
                {
				    $vv="c4.png";
                }
				else
				{
                    $vv="c6.png";
				}
			}
            $val[]=$rid."|".$vv;
            
            $data[]=$vv;
        }
        $i+=1;
	}

    $dat=implode(",",$val);
    $ff=fopen("det.txt","w");
    fwrite($ff,$dat);
    fclose($ff);
	
	
?>

<div style="width:952px; height:402px; background:url(img/road2.png); border:#003366 solid 5px">
						
						<br>
						<br><br>
						<br><br>
						<br><br>
						<br><br>
						<br><br>
						
							<div class="box">
							
							<marquee behavior="scroll" direction="right" height="390" onMouseDown="this.stop();" onMouseUp="this.start();" scrolldelay="10" scrollamount="10">
						<?php
						foreach($data as $img)
						{
						?>
							<?php if($img=="c1.png") { ?>
						<img src="img/c1.png" width="56" height="38">&nbsp;&nbsp;
							<?php } if($img=="c2.png") { ?>
						<img src="img/c2.png" width="56" height="38">&nbsp;&nbsp;
							<?php } if($img=="c3.png") { ?>
						<img src="img/c3.png" width="56" height="38">&nbsp;&nbsp;
							<?php } if($img=="c4.png") { ?>
						<img src="img/c4.png" width="120" height="45">&nbsp;&nbsp;
							<?php } if($img=="c5.png") { ?>
						<img src="img/c5.png" width="149" height="65">&nbsp;&nbsp;
							<?php } if($img=="c6.png") { ?>
						<img src="img/c6.png" width="140" height="65">
							<?php } ?>
						
						<?php
						}
						?>
						</marquee>	
						
						
							</div>
							</div>
						


	<div style="width:100%; height:400px; overflow:auto">
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
	<?php
	$owner=$r3['uname'];
	$name=$r3['name'];
	$vno=$r3['vno'];
	$mobile=$r3['mobile'];
	$device_id=$r3['eei_device'];
	$rn4=rand(1,50);
	$stt=50;
	if($rn4>40)
	{
	$stt=500;	
	}
	else if($rn4>30)
	{
	$stt=200;	
	}
	else if($rn4>15)
	{
	$stt=100;	
	}
	else 
	{
	$stt=50;	
	}
	
	
	
	
	$q4=mysqli_query($connect,"select * from ve_data where value1<$stt order by rand()");
	$r4=mysqli_fetch_array($q4);
	
	$mq=mysqli_query($connect,"select max(id) from ve_vehicle_data");
	$mr=mysqli_fetch_array($mq);
	$id=$mr['max(id)']+1;
	
	$value2=0;
	$ev=$r4['value1'];
	if($ev>200)
	{
	$tn=rand(31,45);
	$value2=$tn;
	}
	else if($ev>100)
	{
	$tn=rand(21,30);
	$value2=$tn;
	}
	else if($ev>50)
	{
	$tn=rand(11,20);
	$value2=$tn;
	}
	else 
	{
	$tn=rand(1,10);
	$value2=$tn;
	}
	
	$qry=mysqli_query($connect,"insert into ve_vehicle_data(id,owner,vno,pm2,pm10,no,no2,nox,nh3,co,so2,o3,value1,rdate,rtime,device_id,value2) values($id,'$owner','$vno','$r4[pm2]','$r4[pm10]','$r4[no]','$r4[no2]','$r4[nox]','$r4[nh3]','$r4[co]','$r4[so2]','$r4[o3]','$r4[value1]','$rdate','$rtime','$device_id','$value2')");
	echo "<br>Vehicle EEI Device ID: ".$r3['eei_device'];
	echo "<br>PM2: ".$r4['pm2'].", PM10: ".$r4['pm10'].", NOx: ".$r4['nox'].", NH3: ".$r4['nh3'];
	echo "<br>SO2: ".$r4['so2'].", CO: ".$r4['co'].", O3: ".$r4['o3'];
	
	
	$q5=mysqli_query($connect,"select * from ve_vehicle_data where vno='$vno' && check_st=0");
	$n5=mysqli_num_rows($q5);
	if($n5>=6)
	{
		while($r5=mysqli_fetch_array($q5))
		{
		$val=$r5['value1'];
			if($val>200)
			{
			$st='4';
			}
			else if($val>100)
			{
			$st='3';
			}
			else if($val>50)
			{
			$st='2';
			}
			else
			{
			$st='1';
			}
			mysqli_query($connect,"update ve_vehicle_data set check_st=$st where id='".$r5['id']."'");
		}
	}
	$q6=mysqli_query($connect,"select * from ve_vehicle_data where vno='$vno' && check_st>0 && status=0");
	$n6=mysqli_num_rows($q6);
	if($n6>0)
	{
	$r6=mysqli_fetch_array($q6);
		$q61=mysqli_query($connect,"select * from ve_vehicle_data where vno='$vno' && check_st=1 && status=0");
		$v1=mysqli_num_rows($q61);
		
		$q62=mysqli_query($connect,"select * from ve_vehicle_data where vno='$vno' && check_st=2 && status=0");
		$v2=mysqli_num_rows($q62);
		
		$q63=mysqli_query($connect,"select * from ve_vehicle_data where vno='$vno' && check_st=3 && status=0");
		$v3=mysqli_num_rows($q63);
		
		$q64=mysqli_query($connect,"select * from ve_vehicle_data where vno='$vno' && check_st=4 && status=0");
		$v4=mysqli_num_rows($q64);
		
		$res="";
		if($v1>$v2 && $v1>$v3 && $v1>$v4)
		{
		$res="Good Condition";
		?><br>Predicted Result: <span style="color:#009900">Good Condition</span><?php
		mysqli_query($connect,"update ve_register set status='$res' where vno='$vno' && uname='$owner'");
		}
		else if($v2>$v3 && $v2>$v4)
		{
		$res="Satisfactory";
		?><br>Predicted Result: <span style="color:#0033CC">Satisfactory</span><?php
		mysqli_query($connect,"update ve_register set status='$res' where vno='$vno' && uname='$owner'");
		}
		else if($v3>$v4)
		{
		$res="Service Required";
		$mess="V.No: $vno, Service Requried";
		?><br>Predicted Result: <span style="color:#FF6600">Service Required</span><?php
		mysqli_query($connect,"update ve_register set service_st=1,status='$res' where vno='$vno' && uname='$owner'");
		echo '<iframe src="http://iotcloud.co.in/testsms/sms.php?sms=emr&name='.$name.'&mess='.$mess.'&mobile='.$mobile.'" width="10" height="10" frameborder="0"></iframe>'; 

		}
		else
		{
		$res="Banned";
		$mess="V.No: $vno, Your Vehicle Banned";
		?><br>Predicted Result: <span style="color:#FF0000">Vehicle Banned</span><?php
		mysqli_query($connect,"update ve_register set ban_st=1,status='$res' where vno='$vno' && uname='$owner'");
		echo '<iframe src="http://iotcloud.co.in/testsms/sms.php?sms=emr&name='.$name.'&mess='.$mess.'&mobile='.$mobile.'" width="10" height="10" frameborder="0"></iframe>'; 

$fp=fopen("loc.txt","r");
$loc=@fread($fp,filesize("loc.txt"));
fclose($fp);

$mess2="V.No: $vno, Vehicle Banned, Loc: ".$loc;
echo '<iframe src="http://iotcloud.co.in/testsms/sms.php?sms=emr&name=RTO&mess='.$mess2.'&mobile='.$mobile2.'" width="10" height="10" frameborder="0"></iframe>'; 

		}
		mysqli_query($connect,"update ve_vehicle_data set status=2 where status=0");
		mysqli_query($connect,"update ve_vehicle_data set result='$res' where vno='$vno' && status=2 && id='".$r6['id']."'");
		
		
		
		?>
		
		<?php
		
	}
	
	?>
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

</div>			
			
<script>
//Using setTimeout to execute a function after 5 seconds.
setTimeout(function () {
   //Redirect with JavaScript
   window.location.href= 'track1.php';
}, 30000);
</script>		
</body>
</html>
