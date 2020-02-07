---
layout: default
---

# Offset as margin

Here are two uneven columns. Notice how each size adds up to 12 max. The number columns plus the offsets equal either 11 or 12 which makes them full width. You can use offsets to create margins at different sizes.

```
<div class="container-fluid">
	<div class="row">
		<div class="d-flex flex-column justify-content-center col-10 offset-1 col-lg-4 offset-lg-1 col-xl-3 offset-xl-2"> </div>
		<div class="d-flex flex-column justify-content-center col-12 offset-0 col-lg-7 offset-lg-0 col-xl-6 offset-xl-1"> </div>
	</div>
</div>
```
