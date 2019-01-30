---
layout: default
---

```js
setInterval(function() {
  var eligible = ["edit-pavement","edit-drainage","edit-structures-bridges-eligible","edit-other","edit-traffic-control-operations","edit-emergency-snow-and-ice-removal","edit-other-emergency-services","edit-engineering","edit-other-traffic-services-roadside-","edit-general-administration-and-miscellaneous-expenditures","edit-rights-of-way-eligible","edit-engineering-where-separable-","edit-construction"];
  var total = ["edit-structures-bridges","edit-emergency-snow-and-ice-removal-total","edit-other-emergency-services-total","edit-engineering-total","edit-other-traffic-services-roadside-total","edit-general-administration-and-miscellaneous-expenditures-total","edit-rights-of-way-total","edit-engineering-where-separable-total","edit-construction-total","edit-traffic-control-operations-total","edit-pavement-total","edit-drainage-total","edit-other-total"];
  var sum_total = 0;
  var sum_elig = 0;

  if(document.getElementById('edit-total-spending') != null){
    for (i = 0; i < total.length; i++) {
      var parsed = parseFloat(document.getElementById(total[i])['value']);
      if(! isNaN(parsed)){
          sum_total = sum_total + parsed;
      }
    }
    console.log("Updated Total Sum: " + sum_total);
    document.getElementById('edit-total-spending')['value'] = sum_total;

    for (i = 0; i < eligible.length; i++) {
      var parsed = parseFloat(document.getElementById(eligible[i])['value']);
      if(! isNaN(parsed)){
          sum_elig = sum_elig + parsed;
      }
    }
    console.log("Updated Eligible Sum: " + sum_elig);
    document.getElementById('edit-actual-spending-on-eligible-facilities')['value'] = sum_elig;
  }
}, 500);
```


```js
if(document.getElementById('view-field-locality-table-column') != null){
  var cells = document.getElementsByTagName("table")[0].rows[1].cells;
  var carryReceipts = cells[1]['innerHTML'].trim().substring(1);
  var newReceipts = cells[2]['innerHTML'].trim().substring(1);
  var totalReceipts = cells[3]['innerHTML'].trim().substring(1);
  document.getElementById('edit-receipt-carry-over-from-previous-year')['value'] = parseFloat(carryReceipts);
  document.getElementById('edit-new-receipts')['value'] = parseFloat(newReceipts);
  document.getElementById('edit-total-receipts')['value'] = parseFloat(totalReceipts);
}
```
