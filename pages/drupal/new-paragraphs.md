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

Basic HTML editor

```
"filter.format.basic_html"
"editor.editor.basic_html"
```

Permissions - `MUST BE CUSTOM TO THE SITE`

```
user.role.editor
user.role.anonymous
user.role.authenticated
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


# Remote Video

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
```
