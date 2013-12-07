There are two suggested data sources for working with AID data. The data from them can be combined in interesting ways to show new insights about Canadian Foreign Aid spending.



The Canadian International Development Platform wraps development data about projects into a OLAP server that can be accessed via a JSON API.  The name of the data cube is 'projects'; usage documentation can be found along with the API at http://cidp.herokuapp.com/

1. IATI Datastore
-----------------

The International Aid Transparency Initiative (IATI) aims to make information about aid spending easier to access. To this end, they publish the IATI Standard and keep a Registry of data in that form.

The IATI Datastore is provided to help users of IATI data access the extracts they are interested in.

The API and use documentation available at http://iati-datastore.herokuapp.com/

2. CIDP API
-----------
Useful API Calls

Get all the CIDIA project data: 
http://cidp.herokuapp.com/cube/cida/facts

Aggregate expenditure amounts, drill down by continent:
http://cidp.herokuapp.com/cube/cida/aggregate?drilldown=continent_name

Aggregate expenditure amounts, drill down by country and/or region:
http://cidp.herokuapp.com/cube/cida/aggregate?drilldown=country_region_name

Drill down by sector
http://cidp.herokuapp.com/cube/cida/aggregate?drilldown=sector_name


Example code:
------------

First, a simple example of how to find sector information using Python

```
# We're interested in all health related sectors. First ask for all sectors
  url = "http://cidp.herokuapp.com/cube/cida/aggregate?drilldown=sector_name"
  data = json.load(urllib2.urlopen(url))
  # Need to build a list of health sector names, and then print out aggregate info for each sector
  print [(c['sector'],c['record_count'],c['amount_sum']) for c in data['cells'] if 'ealth' in c['sector']]

```

Running this code will produce the following list of tuples, containing the Sector Name, the number of projects, and the total funds

```
(u'Health education', 1193, 40902025.194972)
(u'Basic health care', 2292, 501887731.420156)
(u'Reproductive health care', 584, 78442757.3484489)
(u'Basic health infrastructure', 294, 72309202.482159)
(u'Health policy and administrative management', 2662, 172334309.35723)
(u'Health personnel development', 1696, 131600848.03254)
(u'Personnel development for population and reproductive health', 114, 48989087.246)
```
PHP Example

http://cidp-demo.herokuapp.com/ contains a simple example using PHP and Google Charts

An API call is made to the CIDP api, which is reformatted to conform to json format required by Google charts

c

$jsonObject = json_decode(file_get_contents("http://cidp.herokuapp.com/cube/projects/aggregate?drilldown=continent"));


$h1	= array('id'=>'','label'=>'Continent','pattern'=>'','type'=>'string');
$h2 = array('id'=>'','label'=>'Spending','pattern'=>'','type'=>'number');

$headers=array($h1,$h2);
$records=array();
foreach ( $jsonObject->cells as $cell )
{

	 $v1=array('v'=>$cell->continent,'f'=>null);
   	 $v2=array('v'=>round($cell->amount_sum),'f'=>null);
	 $records[]= array('c'=>array($v1,$v2));
}
$new=array();
$new['cols']=$headers;
$new['rows']=$records;
$json = json_encode($new);
echo $json;

```

The Google Charts code can read and display the data without too much fuss.

```
      
    function drawChart() {
      var continentJsonData = $.ajax({
          url: "parseContinentData.php",
          dataType:"json",
          async: false
          }).responseText;

  
      // Create our data table out of JSON data loaded from server.
      var continentData = new google.visualization.DataTable(continentJsonData);
	  var options = {
          title: 'Foreign Aid Spending by Continent',
          width: 800, 
		  height: 600  
        };

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
      chart.draw(continentData, options);

    }

    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <table>
		<tr><td><div id="chart_div"></div></td></tr>
		....
		
```
