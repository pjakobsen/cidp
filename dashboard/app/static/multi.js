jQuery(function($) {
  console.log("hello    ")
  window.dataExplorer = null;
  window.explorerDiv = $('.data-explorer-here');

  // This is some fancy stuff to allow configuring the multiview from
  // parameters in the query string
  //
  
  // For more on state see the view documentation.
  var state = recline.View.parseQueryString(decodeURIComponent(window.location.search));
  if (state) {
    _.each(state, function(value, key) {
      try {
        value = JSON.parse(value);
      } catch(e) {}
      state[key] = value;
    });
  } else {
    state.url = 'demo';
  }
  var dataset = null;
  if (state.dataset || state.url) {
    var datasetInfo = _.extend({
        url: state.url,
        backend: state.backend
      },
      state.dataset
    );
    dataset = new recline.Model.Dataset(datasetInfo);
  } else {
    dataset = new recline.Model.Dataset({
      records: dset,
      // let's be really explicit about fields
      // Plus take opportunity to set date to be a date field and set some labels
      fields: [
        {id: 'id'},
        {id: 'date', type: 'date'},
        {id: 'x', type: 'number'},
        {id: 'y', type: 'number'},
        {id: 'z', type: 'number'},
        {id: 'country', 'label': 'Country'},
        {id: 'title', 'label': 'Title'},
        {id: 'lat'},
        {id: 'lon'}
      ]
    });
  }

  console.log(dataset)

  createExplorer(dataset, state);
});


// make Explorer creation / initialization in a function so we can call it
// again and again
var createExplorer = function(dataset, state) {

  // remove existing data explorer view
  var reload = false;
  if (window.dataExplorer) {
    window.dataExplorer.remove();
    reload = true;
  }
  window.dataExplorer = null;
  var $el = $('<div />');
  $el.appendTo(window.explorerDiv);

  var views = [
    {
      id: 'grid',
      label: 'Grid',
      view: new recline.View.SlickGrid({
        model: dataset
      })
    },
    {
      id: 'graph',
      label: 'Graph',
      view: new recline.View.Graph({
        model: dataset
      })
    },
    {
      id: 'map',
      label: 'Map',
      view: new recline.View.Map({
        model: dataset
      })
    }
  ];

  window.dataExplorer = new recline.View.MultiView({
    model: dataset,
    el: $el,
    state: state,
    views: views
  });
}

