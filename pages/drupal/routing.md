---
layout: default
---

```php
/**
 * Implements hook_menu_local_tasks_alter().
 *
 * Hides the 'Contact' tab on the user profile if the user does not have an
 * email address configured.
 */
function alumni_profile_menu_local_tasks_alter(&$data, $route_name) {
  if ($route_name == 'entity.user.canonical') {
      $data['tabs'][0]['node.edit.aluni_profile'] = [
          '#theme' => 'menu_local_task',
          '#link' => [
              'title' => t('Example tab'),
              'url' => "http://sorensen.dd:8083/user/1",
              'localized_options' => [
                  'attributes' => [
                      'title' => t('Add content'),
                  ],
              ],
          ],
      ];
  }
}
```

It seems that routes and local tasks are defined in the routing.yml files of core and modules.

`entity.user.edit_form`	is the route name that defines the `/user/{user}/edit` user edit link. I want to add a link to the user page that allows for editing of the attached alumni profile.

These entries in `user.links.tasks.yml` define the Edit and View actions for user accounts.

```yaml
entity.user.canonical:
  route_name: entity.user.canonical
  base_route: entity.user.canonical
  title: View
entity.user.edit_form:
  route_name: entity.user.edit_form
  base_route: entity.user.canonical
  title: Edit Account
```


This adds the clone option to the attached profile on the user page in `quick_node_clone.links.tasks.yml` It shows up on the admin edit form.

```yaml
quick_node_clone.node.quick_clone:
  route_name: quick_node_clone.node.quick_clone
  base_route: entity.node.canonical
  title: 'Clone This'
  weight: 30
  ```

It connects to this entry in the `routing.yaml`

```yaml
quick_node_clone.node.quick_clone:
  path: '/clone/{node}/quick_clone'
  defaults:
    _controller: '\Drupal\quick_node_clone\Controller\QuickNodeCloneNodeController::cloneNode'
    _title_callback: '\Drupal\quick_node_clone\Controller\QuickNodeCloneNodeController::clonePageTitle'
  requirements:
    _custom_access: '\Drupal\quick_node_clone\Controller\QuickNodeCloneNodeAccess::cloneNode'
  options:
    _admin_route: TRUE
    parameters:
      node:
        type: entity:node
```

The base route is used to group connected tabs together so if I want to add one to the top of the User page, I need the base_route to be `entity.user.canonical`.

alumni_profile.routing.yaml


This version failed to produce the link needed.

```yaml
alumni.profile_edit_by_alumni:
  path: '/update-your-profile'
  defaults:
    _entity_form: 'node.default'
    _title: 'Update Your Sorensen Alumni Profile'
  requirements:
    _permission: 'edit-own-alumni-profile-content'
    _user_is_logged_in: 'TRUE'
    ```

alumni_profile.links.tasks.yaml

```yaml
alumni.profile_edit_by_alumni:
  route_name: alumni.profile_edit_by_alumni
  base_route: entity.user.canonical
  title: 'Update Alumni Profile'
  weight: 30
```


This user.routing entry sheds some light on what I should be doing. The controller handles the redirection based on the user that is logged in.

```yaml
user.page:
  path: '/user'
  defaults:
    _controller: '\Drupal\user\Controller\UserController::userPage'
    _title: 'My account'
  requirements:
    _user_is_logged_in: 'TRUE'
    ```

The Controller code handles the redirection and specifies the route to take. In this case it is `entity.user.canonical` but for our purposes, we'll use `entity.node.edit_form` and pass the node of the alumni profile as a parameter.

```php
/**
 * Redirects users to their profile page.
 *
 * This controller assumes that it is only invoked for authenticated users.
 * This is enforced for the 'user.page' route with the '_user_is_logged_in'
 * requirement.
 *
 * @return \Symfony\Component\HttpFoundation\RedirectResponse
 *   Returns a redirect to the profile of the currently logged in user.
 */
public function userPage() {
  return $this->redirect('entity.user.canonical', ['user' => $this->currentUser()->id()]);
}
```

So the route will use a controller to handle the redirect.

```yaml
alumni.profile_edit_by_alumni:
  path: '/update-your-profile'
  defaults:
    _controller: '\Drupal\alumni_profile\Controller\AlumniController::route'
    _title: 'Update Your Sorensen Alumni Profile'
  requirements:
    _role: 'administrator'
  options:
    _admin_route: FALSE
```

So with everything looking correct, I still get no menu tasks link added. I suspect it is because there are some access validation checks happening that aren't documented. I want to add teh link to entity.user.canonical but there needs to be a check in the URL for some digits.

[Link to RElated Question online](https://www.drupal.org/forum/support/module-development-and-code-questions/2016-12-19/mymodulelinkstaskyml)

```yaml
I studied a bit the core modules and solved the problem!
The routing.yml file must be like this:

lessons_add_tab:
  path: '/user/{user}/lessons/add'
  defaults:
    _title: 'Add new lesson'
    _form: '\Drupal\mymodule\Forms\LessonsAdd'
  requirements:
    _role: 'instructor + administrator'
  options:
    _admin_route: TRUE
    user: \d+

the last three line are the solution.
Thanks bye
```

Look into the route details to see if there is some info on why my route is a path and not a route that can be added as a menu task. Most of the routes that are like what I want to make are Objects like [entity.node.edit_form](http://sorensen.dd:8083/devel/routes/item?route_name=entity.node.edit_form). I looks like my route needs to use the user account ID in the url to be grouped with the other user tabs.

[More info on the \d+ number validation](https://thinkshout.com/blog/2016/07/drupal-8-routing-tricks-for-better-admin-urls/)

```php
stdClass Object
(
    [__CLASS__] => Symfony\Component\Routing\Route
    [path] => /node/{node}/edit
    [host] =>
    [schemes] => Array
        (
        )

    [methods] => Array
        (
            [0] => GET
            [1] => POST
        )

    [defaults] => Array
        (
            [_entity_form] => node.edit
        )

    [requirements] => Array
        (
            [_entity_access] => node.update
            [node] => \d+
        )

    [options] => Array
        (
            [compiler_class] => \Drupal\Core\Routing\RouteCompiler
            [_node_operation_route] => 1
            [_admin_route] => 1
            [parameters] => Array
                (
                    [node] => Array
                        (
                            [type] => entity:node
                            [converter] => paramconverter.entity
                        )

                )

            [_access_checks] => Array
                (
                    [0] => access_check.entity
                )

        )

    [condition] =>
    [compiled] => stdClass Object
        (
            [__CLASS__] => Drupal\Core\Routing\CompiledRoute
            [fit] => 5
            [patternOutline] => /node/%/edit
            [numParts] => 3
        )
)
```

Mine is a simple array.

```php
Array
(
    [_controller] => \Drupal\alumni_profile\Controller\AlumniController::route
    [_title] => Update Your Sorensen Alumni Profile
    [_route] => alumni.profile_edit_by_alumni
    [_route_object] => stdClass Object
        (
            [__CLASS__] => Symfony\Component\Routing\Route
            [path] => /user/update-your-profile
            [host] =>
            [schemes] => Array
                (
                )

            [methods] => Array
                (
                    [0] => GET
                    [1] => POST
                )

            [defaults] => Array
                (
                    [_controller] => \Drupal\alumni_profile\Controller\AlumniController::route
                    [_title] => Update Your Sorensen Alumni Profile
                )

            [requirements] => Array
                (
                    [_permission] => edit-own-alumni-profile-content
                )

            [options] => Array
                (
                    [compiler_class] => \Drupal\Core\Routing\RouteCompiler
                    [_admin_route] => 1
                    [_access_checks] => Array
                        (
                            [0] => access_check.permission
                        )

                )

            [condition] =>
            [compiled] => stdClass Object
                (
                    [__CLASS__] => Drupal\Core\Routing\CompiledRoute
                    [fit] => 3
                    [patternOutline] => /user/update-your-profile
                    [numParts] => 2
                )

        )

    [_raw_variables] => stdClass Object
        (
            [__CLASS__] => Symfony\Component\HttpFoundation\ParameterBag
            [parameters] => Array
                (
                )

        )
)
```
