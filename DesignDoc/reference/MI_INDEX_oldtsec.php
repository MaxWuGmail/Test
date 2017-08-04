

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=big5">
<script language="javascript">
	function CT(obj,obj2)
	{
		obj.value='';
		obj2.focus();
	}

function KeyinSTKNO(obj)
{
   if(!obj.value&&event.keyCode==32)
		return false;
	else if (event.keyCode == 47) // slash
		return false;
	else if ((event.keyCode >= 48) && (event.keyCode <= 57))    //digit
		return true;
	else if ((event.keyCode >= 65) && (event.keyCode <= 90))    //A-Z
		return true;
	else if ((event.keyCode >= 97) && (event.keyCode <= 122))    //a-z
		return true;
	else 
		return false;
} // end of KeyinSTKNO()


var NowYY, NowMM, NowDD;

function getCurrentDay()
{
	var today = new Date();

	//var temp;
	//temp = today.toGMTString();
	//alert (temp);
	NowYY=today.getYear()-1911;
	NowMM=today.getMonth()+1;
	NowDD=today.getDate();
	dateStr = NowYY + "/";
	if (NowMM <= 9)
	   dateStr = dateStr + "0";
	dateStr = dateStr + NowMM + "/";
	if (NowDD <= 9)
	   dateStr = dateStr + "0";
	dateStr = dateStr + NowDD;
	document.all.input_date.value = dateStr;
}

function check_send()
{
    var i;

    // max user login name 9 char, min user password 5 char
    // use compare use only < or >, no <= or >=
    var max_login_len=10;
    var min_pass_len=5;
    var max_pass_len=9;
    var max_ascii_value = 128;  // ignor basic latin and latin-1 supplement characters
    var doubleByteValue;
    var actual_length=0;

    //check for empty data
    if(document.login_form.input_date.value == "")
    {
      alert("請輸入日期");
      return false;
    }

    return true;
}

function KeyinDate(obj)
{

   if(!obj.value&&event.keyCode==32)
		return false;
	else if (event.keyCode == 47) // slash
		return true;
	else if ((event.keyCode >= 48) && (event.keyCode <= 57))    //digit
		return true;
	else 
		return false;
} // end of KeyinDate()

function checkDate()
{

	str_date = String(date_form.input_date.value);
   
   var i=0, firsti=0, lasti=0, j=0;
   var tmp;
   var tmp_date = new Array();
   tmp_date[0]="00";
   tmp_date[1]="00";
   tmp_date[2]="00";
   
   while (i<str_date.length)
   {
   	tmp=str_date.charAt(i);
   	i++;
   	if (tmp=="/")
   	{
   		lasti=i-1;
   		tmp_date[j]=str_date.substring(firsti, lasti);
   		j++;
   		firsti=i;
   	}	
   }

   tmp_date[j]=str_date.substring(firsti, str_date.length);
 	//alert(str_date);
 	
   var_year = parseInt(tmp_date[0],10);
   var_month = parseInt(tmp_date[1],10);
   var_day = parseInt(tmp_date[2],10);
 	
 	   
   if (var_year < 60 || var_year > 120)
   {
   	alert("輸入錯誤(年):範例:93/12/02");
      return false;
   }
   if (var_month <= 0 || var_month > 12)
   {
   	alert("輸入錯誤(月):輸入範例:93/12/02");
      return false;
   }
   if (var_day <= 0 || var_day > 31)
   {
   	alert("輸入錯誤(日):輸入範例:93/12/02");
      return false;
   }
   // Check Day31 for month 4,6,9,11
   if ((var_day == 31) && (var_month == 4 || var_month == 6 || var_month==9 || var_month==11))
   {
   	alert("查無輸入日期");
      return false;
   }
   // Check Leap year for Feb
   if ((var_day == 31 || var_day == 30) && (var_month == 2))
   {
   	alert("查無輸入日期");
      return false;
   }
   if ((var_day == 29) && (var_month == 2))
   {
      var_year2 = var_year+1911;
      if ( ((var_year2 % 400)==0) ||((var_year2 % 4)==0) && ((var_year2 % 100)!=0) )
         ;
      else
      {
      	alert("查無輸入日期");
         return false;
      }
   }

   dateStr = var_year + "/";
   if (var_month <= 9)
      dateStr = dateStr + "0";
   dateStr = dateStr + var_month + "/";
   if (var_day <= 9)
      dateStr = dateStr + "0";
   dateStr = dateStr + var_day;
   document.all.input_date.value = dateStr;
   
   //alert(str_date);
   
   return true;
} // end of checkdate()

function MM_openBrWindow(theURL,winName,features) 
{ 
	dateStr = showModalDialog("/ch/trading/inc/Calendar.htm","請選擇日期","dialogWidth:17em;dialogHeight:18em");
	if (dateStr)
		document.all.input_date.value = dateStr;
}
</script>
<title>TWSE 臺灣證券交易所 ﹥交易資訊 ﹥盤後資訊 ﹥每日收盤行情</title>

</head>


<body>
<style type="text/css">
<!--
body {
	margin-left: 0px;
	margin-top: 0px;
	margin-right: 0px;
	margin-bottom: 0px;
}
-->
</style>
<link href="/ch/css/style.css" rel="stylesheet" type="text/css">
<link href="/ch/css/oldreport.css" rel="stylesheet" type="text/css">          
			<table width='590' border='0' align='center' cellpadding='0' cellspacing='0'>
              <!--<tr>
                <td><div align='center'></div>
                    <img src='/ch/trading/exchange/images/trading_pic.jpg' width='590' height='90'></td>
              </tr>-->
              <tr>
                <td height='10'><div align='center'> </div></td>
              </tr>
              <tr>
                <form name="date_form" method="post" onsubmit="return checkDate();" action='/ch/trading/exchange/MI_INDEX/MI_INDEX_oldtsec.php'><td><div align='center'>
                    <table width='590' border='0' cellpadding='0' cellspacing='0'>
                      <tr bgcolor='#EBDCC9'>
                        <td height='40' class='basic2'><div align='right'><font size='2'>&#12288;資料日期：
                                  <input type="text" class='board' name="input_date" maxlength="10" size="12" OnKeyPress="return KeyinDate(this);" value=""> <img src="/ch/trading/images/data.gif" onClick="MM_openBrWindow('.html','輸入日期','width=230,height=220')" width="16" height="16" style="cursor:hand"> </font>
								  <font size='2'>&#12288;分類項目：
                                  <select name='select2' class='board'>
									
<option  selected  value='MS'>大盤統計資訊</option><option  selected  value=''>全部</option><option   value='00'>基金</option><option   value='00P'>ETF</option><option   value='05'>認購權證</option><option   value='05P'>認售權證</option><option   value='11'>水泥工業</option><option   value='12'>食品工業</option><option   value='13'>塑膠工業</option><option   value='14'>紡織纖維</option><option   value='15'>電機機械</option><option   value='16'>電器電纜</option><option   value='17'>化學生技醫療</option><option   value='18'>玻璃陶瓷</option><option   value='19'>造紙工業</option><option   value='20'>鋼鐵工業</option><option   value='21'>橡膠工業</option><option   value='22'>汽車工業</option><option   value='23'>電子工業</option><option   value='25'>建材營造</option><option   value='26'>運輸業</option><option   value='27'>觀光事業</option><option   value='28'>金融保險</option><option   value='29'>貿易百貨</option><option   value='91'>存託憑證</option><option   value='98'>綜合企業</option><option   value='99'>其他</option><option   value='CB'>可轉換公司債</option>                                  </select>
                                  </font><font size='2'> &#12288;
                                  <input name="login_btn" type="submit" value=" 查詢 " OnClick="return checkDate();">
                              </font></div>
							  </td>
							  </tr>
							  <tr>
							  <td class='til_2' align=right>
							  民國93年2月11日起之資料請回原網站查詢
							  <!--&#12288;本資訊自民國-1911年0月0日起開始提供，民國89年1月1日至-1911年0月-1日資訊<a href="#" onClick="window.open('/ch/trading/exchange/MI_INDEX/MI_INDEX_oldtsec.php?input_date=','','toolbar=no,location=no,menubar=no,status=no,directories=no,resizable=yes,scrollbars=yes');">由此查詢</a>-->
								</td>
                      </tr>
                    </table>
                </div></td></form>
              </tr>
              <tr>
                <td height='10'><div align='center'></div></td>
              </tr>
            </table>
        </div></td>
      </tr>
    </table>
    <center>
    <table align='center' width='590' border='0' cellpadding='0' cellspacing='0'><tr><td align='left' class='til_2'>查無資料 : 0年月日 </td></tr></table>    </center>                
</body>

</html>