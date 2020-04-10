# General Sync - In sections

Allow remote video to appear in additional content as well as column content.
```                       
"field.field.paragraph.bp_columns_two_uneven.bp_column_content_2"
"field.field.paragraph.bp_columns.bp_column_content"              
"field.field.node.page.field_paragraphs"
"field.storage.paragraph.bp_column_content_2"                     
"field.storage.paragraph.bp_column_content"
```

View for seeking out advanced HTML pages
```
"views.view.pages_with_advanced_html"
```

Basic HTML editor and Advanced

```
"filter.format.basic_html"
"editor.editor.basic_html"
"filter.format.full_html"
"editor.editor.full_html"
```

Permissions - `MUST BE CUSTOM TO THE SITE`

```
user.role.editor
user.role.anonymous
user.role.authenticated
```

# Editor Folder

```
"views.view.pages_with_advanced_html"
"filter.format.basic_html"
"editor.editor.basic_html"
"filter.format.full_html"
"editor.editor.full_html"
```

# Media Storage

```
"field.storage.media.field_media_file"
"field.field.media.file.field_media_file"
"field.field.media.video.field_media_video_file"
"field.field.media.image.field_media_image"
"field.storage.media.field_media_image  "
"field.storage.media.field_media_video_file"
"field.storage.media.field_media_audio_file"
"field.field.media.audio.field_media_audio_file"
```

# Flex Grid - All New Files

```
"paragraphs.paragraphs_type.flex_grid"
"paragraphs.paragraphs_type.flex_grid_1_4"
"paragraphs.paragraphs_type.flex_grid_child"
"field.field.paragraph.flex_grid_child.field_flex_link"
"field.field.paragraph.flex_grid_child.field_flex_image"
"field.field.paragraph.flex_grid_child.field_flex_child"
"field.storage.paragraph.field_flex_link"
"field.storage.paragraph.field_flex_child"
"field.storage.paragraph.field_flex_body"
"field.field.paragraph.flex_grid_1_4.field_flex_grid_child"
"field.field.paragraph.flex_grid_child.field_flex_body"
"core.entity_view_display.paragraph.flex_grid.default"
"core.entity_form_display.paragraph.flex_grid.default"
"core.entity_view_display.paragraph.flex_grid_1_4.default"
"core.entity_form_display.paragraph.flex_grid_1_4.default"
"core.entity_view_display.paragraph.flex_grid_child.default"
"core.entity_form_display.paragraph.flex_grid_child.default"
"field.field.paragraph.flex_grid.field_flex_grid_child"
"field.storage.paragraph.field_flex_grid_child"
"field.storage.paragraph.field_flex_image"
"field.field.paragraph.flex_grid_child.field_flex_body"
```


# Youtube Video

```
"paragraphs.paragraphs_type.remote_video"    
"field.storage.paragraph.field_youtube_video"
"field.field.paragraph.remote_video.field_youtube_video"
"core.entity_view_display.paragraph.remote_video.default"         
"core.entity_form_display.paragraph.remote_video.default"
```

These are associated with allowing the remote video field to be included in other sections. These config files allow you to add the remote video to a basic page, two equal columns, and two uneven columns.

```         
"field.storage.paragraph.bp_column_content_2"                     
"field.storage.paragraph.bp_column_content"                       
"field.field.paragraph.bp_columns_two_uneven.bp_column_content_2"
"field.field.paragraph.bp_columns.bp_column_content"              
"field.field.node.page.field_paragraphs"      
```

# Spotlight Section

New Files
```
"field.storage.paragraph.field_spotlight_section_title"            
"field.storage.paragraph.field_spotlight_link"                     
"field.storage.paragraph.field_spotlight_image"                    
"field.storage.paragraph.field_spotlight_body"                     
"field.storage.paragraph.field_spotlight_background_color"         
"paragraphs.paragraphs_type.spotlight"                             
"field.field.paragraph.spotlight.field_spotlight_section_title"    
"field.field.paragraph.spotlight.field_spotlight_link"             
"field.field.paragraph.spotlight.field_spotlight_image"            
"field.field.paragraph.spotlight.field_spotlight_body"             
"field.field.paragraph.spotlight.field_spotlight_background_color"
"core.entity_view_display.paragraph.spotlight.default"             
"core.entity_form_display.paragraph.spotlight.default"             
```

Files updated or modified
```
field.field.node.page.field_paragraphs
user.role.editor
user.role.anonymous
user.role.authenticated
```

# News Update

Fields that are required to create the news update content type.
```
"field.storage.node.field_news_update_image"            
"node.type.news_update"                                 
"field.field.node.news_update.field_news_update_image"  
"field.field.node.news_update.body"
"field.field.node.news_update.field_news_update_additional_con"
"field.storage.node.field_news_update_additional_con"                     
"core.entity_form_display.node.news_update.default"     
"core.entity_view_display.node.news_update.teaser"      
"core.entity_view_display.node.news_update.default"  
```

Block Configuration for the news update block. The view creates the block.

```
"views.view.news_updates"
"views.view.news_updates_full_grid"
"block.block.views_block__news_updates_full_grid_block_1"
"block.block.views_block__news_updates_block_1"
"core.menu.static_menu_link_overrides"
```

# Demographics Config Updates -> prepare large config set

These need to be copied to the next site.
Go ahead and `paste them into the prepare_large_config_fileset bash file`

```
"block.block.views_block__news_updates_block_1"
"block.block.views_block__news_updates_full_grid_block_1"
"core.entity_view_display.media.image.default"
"editor.editor.basic_html"
"filter.format.basic_html"
"views.view.news_updates"
"views.view.news_updates_full_grid"
"views.view.pages_with_advanced_html"

DO NOT ADD MORE TO THIS BLOCK
```

Hiding the help button in the menu added this to `core.menu.static_menu_link_overrides`

```
help__main:
  menu_name: admin
  parent: system.admin
  weight: 9
  expanded: false
  enabled: false
```

These are harder to deal with. For now they need to be handled custom.
```
user.role.editor
```

# Finished Demographics Config - put it all in large-1

Hero Video, Employee profiles improved links, and News Updates

```
"field.storage.node.field_tagline"                                        
"field.storage.node.field_related_employee_profiles"                      
"field.storage.node.field_news_update_external_link"                      
"field.storage.node.field_hero_video_direct_link"                         
"field.field.node.news_update.field_news_update_external_link"            
"field.field.node.page.field_tagline"                                     
"field.field.node.page.field_hero_video_direct_link"                      
"field.field.node.news_update.field_related_employee_profiles"            
"block.block.views_block__news_updates_block_2_specific_employee_profile"
"field.storage.node.field_additional_links"                                                                    
"field.field.node.news_update.field_news_update_image"            
"field.field.node.profile.field_profile_twitter"                  
"field.field.node.profile.field_profile_linkedin"                 
"field.field.node.profile.field_profile_facebook"                 
"field.field.node.profile.field_additional_links"                 
"block.block.testvirginiapopulationestimatesinteractivemap"                                                                                                                  
"core.entity_form_display.node.page.default"                 
"core.entity_form_display.node.news_update.default"              
"core.entity_view_display.node.page.teaser"                       
"core.entity_view_display.node.page.default"                 
"core.entity_view_display.node.news_update.teaser"                
"core.entity_view_display.node.news_update.default"               
"views.view.news_updates"                                         
"block.block.views_block__news_updates_block_1"                   
"views.view.news_updates_full_grid"                               
"block.block.views_block__news_updates_full_grid_block_1"
```          
