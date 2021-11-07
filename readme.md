# 环境配置（可忽略）

如果想要预览效果需要安装以下工具：

-   texlive
-   python 及其依赖 pygments
-   vscode 以及插件 Tex Workshop、Vscode Google Translate（用于辅助翻译）

如果只是翻译，英文原本请查阅 output/main.pdf 文件

# 进度

```text
├─0_preface 大量机翻，需订正
│      0_0_0_viewing_markdown_files.tex
│      0_0_an_ecosystem_for_modern_web_applications.tex
│      0_1_target_audience.tex
│      0_2_benefits_of_understanding_the_source.tex
│      0_3_accessing_the_source.tex
│      0_4_keeping_up_to_date.tex
│      0_preface.tex
│
├─1_internals_of_zone_js 大量机翻，需订正
│      1_0_0_project_information.tex
│      1_0_overview.tex
│      1_1_0_use_within_angular.tex
│      1_1_using_zone_js.tex
│      1_2_0_relationship_between_zone_zonespec_zonedelegate_interfaces.tex
│      1_2_api_model.tex
│      1_3_0_root_directory.tex
│      1_3_1_dist.tex
│      1_3_2_example.tex
│      1_3_3_scripts.tex
│      1_3_source_tree_layout.tex
│      1_4_0_zone_ts.tex
│      1_4_source_model.tex
│      1_internals_of_zone_js.tex
│
├─2_tsickle 大量机翻，需订正
│      2_0_overview.tex
│      2_1_source_tree_layout.tex
│      2_2_the_src_sub_directory.tex
│      2_tsickle.tex
│
├─3_ts_api_guardian 大量机翻，需订正
│      3_0_overview.tex
│      3_1_usage.tex
│      3_2_source_tree.tex
│      3_3_bin.tex
│      3_4_lib.tex
│      3_ts_api_guardian.tex
│
├─4_rxjs 大量机翻，需订正
│      4_0_introduction.tex
│      4_1_project_information.tex
│      4_2_api_model.tex
│      4_3_0_files_in_root_directory.tex
│      4_3_source_tree_model.tex
│      4_rxjs.tex
│
├─5_the_core_package
│      5_0_overview.tex
│      5_10_0_source_tree.tex
│      5_10_core_zone_feature_core_src_zone.tex
│      5_11_0_core_testability_public_api.tex
│      5_11_1_core_testability_usage.tex
│      5_11_2_core_testability_implementation.tex
│      5_11_core_testability_feature_core_src_testability.tex
│      5_12_0_core_linker_public_api.tex
│      5_12_1_core_linker_usage.tex
│      5_12_2_core_linker_implementation.tex
│      5_12_core_linker_feature_core_src_linker.tex
│      5_13_0_private_exports_api.tex
│      5_13_1_core_view_implementation.tex
│      5_13_core_view_feature_core_src_view.tex
│      5_1_core_public_api.tex
│      5_2_source_tree_layout.tex
│      5_3_0_core_src.tex
│      5_3_1_core_src_util.tex
│      5_3_source.tex
│      5_4_core_dependencyinjection_feature_core_src_di.tex
│      5_5_core_metadata_feature_core_src_metadata.tex
│      5_6_core_profile_feature_core_src_profile.tex
│      5_7_core_reflection_feature_core_src_reflection.tex
│      5_8_0_core_src_debug.tex
│      5_8_core_render_feature_core_src_render.tex
│      5_9_core_changedetection_feature_core_src_change_detection.tex
│      5_the_core_package.tex
│
├─6_the_common_package
│      6_0_overview.tex
│      6_1_common_public_api.tex
│      6_2_source_tree_layout.tex
│      6_3_0_common_src.tex
│      6_3_1_common_src_i_n.tex
│      6_3_2_common_src_directives.tex
│      6_3_3_common_src_location.tex
│      6_3_4_common_src_pipes.tex
│      6_3_source.tex
│      6_the_common_package.tex
│
├─7_the_common_http_sub_package
│      7_0_common_http_public_api.tex
│      7_1_0_http_src.tex
│      7_1_source_tree_layout.tex
│      7_the_common_http_sub_package.tex
│
├─8_the_platform_browser_package
│      8_0_overview.tex
│      8_1_platform_browser_public_api.tex
│      8_2_source_tree_layout.tex
│      8_3_0_platform_browser_src.tex
│      8_3_1_platform_browser_src_dom.tex
│      8_3_2_platform_browser_src_browser.tex
│      8_3_3_platform_browser_src_security.tex
│      8_3_source.tex
│      8_the_platform_browser_package.tex
│
├─9_the_platform_browser_dynamic_package
│      9_0_overview.tex
│      9_1_platform_browser_dynamic_api.tex
│      9_2_source_tree_layout.tex
│      9_3_0_src.tex
│      9_3_1_src_resource_loader.tex
│      9_3_source.tex
│      9_the_platform_browser_dynamic_package.tex
├─10_the_platform_server_package
│      10_0_overview.tex
│      10_1_platform_server_api.tex
│      10_2_source_tree_layout.tex
│      10_3_0_platform_server_src.tex
│      10_3_source.tex
│      10_the_platform_server_package.tex
│
├─11_the_platform_webworker_package
│      11_0_overview.tex
│      11_1_platform_webworker_public_api.tex
│      11_2_source_tree_layout.tex
│      11_3_0_platform_webworker_src.tex
│      11_3_1_platform_webworker_src_web_workers.tex
│      11_3_source.tex
│      11_the_platform_webworker_package.tex
│
├─12_the_platform_webworker_dynamic_package
│      12_0_overview.tex
│      12_1_platform_webworker_dynamic_api.tex
│      12_2_source_tree_layout.tex
│      12_the_platform_webworker_dynamic_package.tex
│
├─13_the_router_package 大量机翻，需订正
│      13_0_overview.tex
│      13_1_router_api.tex
│      13_2_source_tree_layout.tex
│      13_3_0_router_src.tex
│      13_3_1_router_src_directives.tex
│      13_3_source.tex
│      13_the_router_package.tex
│      router_api_1.png
│      router_api_2.png
│      router_api_3.png
│
├─14_render_ivy_in_angular 大量机翻，需订正
│      14_0_preliminaries_paths_and_names.tex
│      14_1_0_public_documentation.tex
│      14_1_overview.tex
│      14_2_0_impact_enableivy_has_on_angular_cli_s_code_generation.tex
│      14_2_the_angular_cli_and_enableivy.tex
│      14_3_render_in_the_compiler_cli_package.tex
│      14_4_render_in_the_compiler_package.tex
│      14_5_0_api_model.tex
│      14_5_1_source_model.tex
│      14_5_2_interfaces.tex
│      14_5_render_in_the_core_package.tex
│      14_render_ivy_in_angular.tex
│
└─15_the_forms_package 大量机翻，需订正
       15_0_overview.tex
       15_1_forms_api.tex
       15_2_source_tree_layout.tex
       15_3_0_forms_src.tex
       15_3_source.tex
       15_the_forms_package.tex
       forms_api_accessors.png
       forms_api_directives.png
       forms_api_main.png
       forms_api_validator.png
       form_control_hierarchy.png
```

# 步骤

进入 zh/ 目录下，翻译对应章节，将被 % 注释掉的英文文本翻译成中文即可。
