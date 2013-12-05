There are two suggested data sources for working with AID data. The data from them can be combined in interesting ways to show new insights about Canadian Foreign Aid spending.

2. IATI Datastore
-----------------

The International Aid Transparency Initiative (IATI) aims to make information about aid spending easier to access. To this end, they publish the IATI Standard and keep a Registry of data in that form.

The IATI Datastore is provided to help users of IATI data access the extracts they are interested in.

The API and use documentation available at http://iati-datastore.herokuapp.com/

Example:
--------

http://cidp-demo.herokuapp.com/ contains a simple example using PHP and Google Charts

An API call is made to the CIDP api, which is reformatted to conform to json format required by Google charts

'''

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

'''

The Google Charts code can read and display the data without too much fuss.

'''
      
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
		
'''


++++++++++++++++++
Using the CIDP API
++++++++++++++++++

The API is located at http://cidp.herokuapp.com

This API uses JSON: 

Looking at API Meatadata, the structure of the API:
---------------------------------------------------

The best way to examine the result is to install JSONView for Chrome
or to use python json mtool

It is a cube model. You can examine the cube by asking the OLAP server for it's application model:

http://cidp.herokuapp.com/model

You can also get a list of the cubes.  Each data source has a cube

http://cidp.herokuapp.com/model/cubes

So far, the model contains only 1 cube, projects. 

http://cidp.herokuapp.com/model/cube/projects

Projects have 5 dimensions:

http://cidp.herokuapp.com/model/cube/projects/dimensions

"project",
"year",
"amount",
"continent",
"sector"

You can look at a single dimension:

http://cidp.herokuapp.com/model/dimension/sector

http://cidp.herokuapp.com/model/dimension/sector

Browsing and Aggregation
------------------------

/cube/<cube_name>/<browser_action> where the browser action might be aggregate, facts, fact, dimension and report.

For example: 

http://cidp.herokuapp.com/cube/projects/aggregate

http://cidp.herokuapp.com/cube/projects/aggregate?drilldown=continent