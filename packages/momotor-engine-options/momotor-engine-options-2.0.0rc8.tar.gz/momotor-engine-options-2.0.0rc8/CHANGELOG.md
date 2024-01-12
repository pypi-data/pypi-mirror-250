# Changelog

<!--next-version-placeholder-->

## v1.1.1 (2023-08-29)

### Fix

* Regression: preflight option selector placeholders are not expanded ([`bdfa8c0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/bdfa8c09ef7544342e4aaa451ce2bed7a834a207))

## v1.1.0 (2023-08-29)

### Feature

* Add json style preflight status ([`a346c6d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/a346c6d09905b92f61cbaaae39795e1d2aaddd43))

### Fix

* Emulate LabelOptionMixin's handling of the label option when preflight causes step to not execute ([`6383900`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/63839005e2e5ea4d401330fbc25c4e3e28ff94e9))

## v1.0.0 (2023-07-06)

### Feature

* Support sub versions (dashed suffixes) in tool versions, to support Anaconda 2023.03-1 ([`aee2c3f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/aee2c3f1d266b78deb2c2a8bb20c756cb382d361))

### Breaking

* Dropped Python 3.7 support ([`e1a3d05`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/e1a3d05abcfbaaec61b24ad21e94e599e1e869c3))

## v0.10.1 (2023-06-19)

### Fix

* Some error messages were incomplete/cryptic ([`3b37a8c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/3b37a8c1a2998e68b0661ff3999d4ab41a063571))

## v0.10.0 (2022-11-15)
### Feature
* Add 'pass-hidden' and 'fail-hidden' preflight actions ([`c749a05`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/c749a0560083ee6395ccdb829714626ff1f67796))

## v0.9.1 (2022-10-27)
### Fix
* Strip leading and trailing whitespace from selectors and references ([`929d233`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/929d23349700132234848921ed19de1f16628374))

## v0.9.0 (2022-10-21)
### Feature
* Restore `!` selector operator ([`d4581ba`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/d4581ba2bbb5356e12c639597396eafe76d0acf4))

## v0.8.0 (2022-10-06)
### Feature
* Add optional dimensions to `tasks@scheduler` option ([`9a4c768`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9a4c7684392c10b9dfbc43d4525335ca3d2e1b60))

## v0.7.0 (2022-07-19)
### Feature
* Add key-value list parser ([`825d5ac`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/825d5ac277b3d687a4a2b0d1190a6dfdc047b307))

## v0.6.0 (2022-07-07)
### Feature
* Add `sumf` and `sumr` modifiers ([`533f0cb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/533f0cb7033cc2ff5d4e005852bd75b259ae7923))
* Add `empty_values` argument to `convert_intlist` ([`6be2ea1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/6be2ea14c10d60fb2967424fe691df28eb95ed5f))
* Add convert.convert_intlist ([`9a071c8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9a071c8816ea8e913baac322ab409bafe8fb7bd8))
* Update ToolName.factory to accept a deconstructed tool base name and versions list ([`7d1b8e2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/7d1b8e283d9c99bd3ab5effc03f9d0692fbb7267))

### Fix
* Handle tool options provided as child content ([`1a99ffb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/1a99ffbbcbafdaba7e2451dec8e5bf46ee893e6a))
* Relax task reference parsing even more. the initial dot is now not required anymore. the $ and internal operators can be escaped to ignore them ([`f353e7d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/f353e7d6d52f772f76c326611bdbdb5513b8113b))
* Relax task reference parsing, allowing trailing text immediately after the references without a dot as seperator ([`829b40c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/829b40cee42ad376d4d000d3a3f0f780953eac94))
* Expand task-id placeholders in references ([`545a619`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/545a619b495e7ab0f9c12d9ee4b9ab41b77d1c76))
* Support placeholders in tool options ([`796f3ce`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/796f3ce75ebc404e08f86234154270215357c3fb))

## v0.5.0 (2022-04-08)
### Feature
* Add duration and size conversion methods ([`424815f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/424815fcc9c57d2e62dbd79e017e5e039a660a62))

### Fix
* Correct option type usage and handling ([`2a0a537`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/2a0a537a2d2dfdab43fa3ab49c6c355c41170311))
* Use option types as defined by the momotor-bundles package ([`e53b4c3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/e53b4c3fddc5dd03ea18d8d99a87c19d3012c50f))

## v0.4.0 (2022-04-04)
### Feature
* Add OptionDefinition.deprecated ([`9a98031`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9a98031723833fc5717027b56d890f47f3bd0e76))

## v0.3.0 (2022-03-14)
### Feature
* Added `match_tool_requirements`. Also refactored types ([`2dd834b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/2dd834be877c596ea79f7ee68ae55b43d67f07c9))
* Add ToolRequirements type alias, cleanup imports ([`5012876`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/50128762927fae7413f0658feb92c3b12841ac61))
* Add momotor.options.domain.scheduler.tools.get_scheduler_tools_option ([`3f16a99`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/3f16a9983a59d85fec01d326de8b8b84c9adf8a7))
* Allow multiple version preferences to be supplied in the tools option ([`4f4f6ba`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/4f4f6ba55bbf284213ed502bbfa9a4fc3c05ab9b))
* Add ToolOptionDefinition ([`ab5f387`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ab5f387b64c71fb6e853c0532b98a3baf73b65ef))
* Add function to match tool from a list of alternatives ([`1c25d2d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/1c25d2d95100f2a541fb1a931ac9b5a2be8342e2))
* Allow parts of tool name to be a wildcard when resolving, correctly merge versions in multiple registries ([`1064f69`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/1064f69247445dc87f77e46cc543f355f4e3eb38))
* Add functions to access tool registry ([`935d0df`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/935d0dfc9184a9fd6fa90b9469d104b4dad1b2d7))

### Fix
* Add more unit tests for cases with defaults ([`fd425a2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/fd425a211f4d34bbc10b9a1d84204d5f4563ca26))
* Hide hidden fields from repr ([`cddbd6f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/cddbd6fc8cac215343cd39001d3e3bc1f7f7ec27))
* ToolVersion.is_partial should also return True if either version is DEFAULT ([`fd382f8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/fd382f8d6ddc20f135d258743c1049bb1a588aa8))
* Unit tests ([`b2a2871`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/b2a28712077097c0ff74c15edfbaad33f65241e9))
* Set fixed location for tools domain options, use ToolName.SEPARATOR constant ([`d7db33a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/d7db33a97e6f0020c9cc7c7aee8a806d5f330945))
* Consistent argument naming ([`b0f8af5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/b0f8af5cf430acbdc490309159f65d6b5cb73e6b))
* Correctly handle symlinks in registry ([`3b70e30`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/3b70e30860a3f7c5c1cbf5a6b11338e0c45f7d0a))
* Unit test ([`7755c6e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/7755c6e24bd0589d4f9ad7967d77c4fb6346cda4))
* Various fixes, cleanups and changes ([`273a1ea`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/273a1ea7ee741dcd1de266328e1a2e2b9adcbf4f))
* Move NO_DEFAULT into OptionDefinition ([`7382692`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/73826926ea91293d249b7cef8b2491fba12903ea))
* Make Tool.name the resolved name, add Tool.__hash__ ([`3d084a5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/3d084a5bc97f5b51ca4dabd9ae0ad147075f3119))
* When numeric versions and named versions are mixed, the numeric versions should be preferred over named versions ([`b352fce`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/b352fce768044ef910df9c1b27e58fccf6c57b67))
* Use `_default` as default tool version or name ([`cc551de`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/cc551de6a5aecfffeaee3404d983d95dedf9f9fb))
* Add SimpleVersion.__str__ for consistency with ToolName ([`0b37ae0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/0b37ae0453a937cbed346ae7a7769ed1b78f94e4))
* ToolName and SimpleVersion hash should be based on version(s) ([`69eae79`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/69eae79300e808f052842a807abb8e9c207800ee))
* Match_tool should return the exact value from tools argument ([`ed324ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ed324abf0dc848485e54bdc40655c1a5e6d4ae20))
* Convert tool_info.name to str ([`ba157aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ba157aa1ea007c9a4ce324542c839bd6a7475ee3))
* Correct handling of version directories ([`785d674`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/785d67403012facd45c5483d59d8a54a7b66cf03))

## v0.2.3 (2022-01-24)
### Fix
* Replace_placeholders() should accept any non-string value argument ([`0035b68`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/0035b6854bbd37decdbabf25c2132eace308cc27))

## v0.2.2 (2022-01-21)
### Fix
* Add unittests for all combiner modifiers, fix issues with the combiner modifiers ([`adc6475`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/adc6475dfe54d85871b554d6b3da3aba433c61c4))

## v0.2.1 (2022-01-18)
### Fix
* Use 'skip-error' action as default error action ([`c98e3da`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/c98e3da587ecaed17c935e21f11800f34787031c))
* Include options from step in preflight result ([`ba5070b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ba5070b8335732ab8849e5afc6eeafe7bc09134f))

## v0.2.0 (2022-01-18)
### Feature
* Added 'no' match modifier, removed '!' operator ([`39f6f12`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/39f6f1229a881d27688a9684de75325cbf3317be))
* Allow multiple providers in references (close #9) ([`9ae0b1a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9ae0b1afeec9c250d828b4e917c8618091d1b343))

### Fix
* Make %not an alias for %notany ([`0884717`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/088471781b977985976019b2baaa31d7ee297fd3))
* Change 'no'/'none' into 'notall'/'notany', implement same for value references ([`0599591`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/05995916a914e68d02080458e9166e7ade1f9ef6))
* Handle invalid selectors ([`e136e41`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/e136e410b699bed4f4c9b55528b9284aba99469a))
* Correctly handle option domain defaults ([`11e3ca8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/11e3ca85192802e6a472d6fa265e167eeaca19d0))
* Handle ids with wildcards in references (closes #7) ([`9370fe8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9370fe8dffd8e112bfdfc22a8de7f33a50443ad5))
* Add logging ([`0369311`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/0369311bb5c94d00c8b139d09aa958b35476d6a3))
* Preflight option can have mod ([`208ac07`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/208ac079b28c29773fe6403c81db2a66915037c8))

## v0.1.0 (2022-01-17)
### Feature
* Generate default option subdomains (closes #7) ([`8e39f09`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/8e39f0954b5c3b982b9a651dca2632d2d9cbf28a))
* Add 'always' preflight option action ([`5459dcb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/5459dcbbc12d2c60239a3b028f97f2adcbf8d832))
* Allow OptionDefinition.name to be an OptionNameDomain object ([`eb9da99`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/eb9da99dfc82383bf720b0cce1f8f3252355aa48))
* Restore the select_by_XXX_reference methods ([`e7ce22b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/e7ce22bf3d89d2f50e659b6366fe19681de751da))
* Add argument to change default modifier for resolve_value_reference ([`59bbe20`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/59bbe20b94c582c432dc83e081487cde2f9ea685))
* Add `result` reference type ([`ac52431`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ac52431385fb98c0cae276470396a8df2f656cbb))
* Replace placeholders in tasks@scheduler option ([`72798b9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/72798b93afe10488e0c60e87d82e0b940966153b))
* Restored filter_result_query function ([`e20003a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/e20003af48e9313ea170a1f1d72bf3c691c9d2b1))
* Add `value_processor` to apply_template ([`3dabf78`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/3dabf78e4bc82139e99f0aac694a5a8778184f12))
* Make OptionsProviders more generic and also use it for the parsers ([`f03bd77`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/f03bd77778155d27de43025c4abe6d680799dc7c))
* Add task-number expansion ([`16f6442`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/16f64425e5e44243b42e013f16107065e01fe5d4))
* Add '!' and '!=' operations since there is no more "not-prop" type ([`cc3b698`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/cc3b69836ffa3e50138e68214ad7972310cc51d0))
* Add template parser ([`cd7c1ea`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/cd7c1ea1896e121aaf8d9202a2cb692c8e9be8d7))
* Add new selector methods ([`0d30ac5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/0d30ac5005124b3e3c6324b112bb0e733f481991))
* Change reference resolver to return both the containing element and the resolved objects ([`9f8f054`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9f8f05452e853f7a7d8135fda8db6d5b0d3e1c83))
* Add generalized parser and resolvers for outcome/property/file/option references ([`03a6dc1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/03a6dc1df9b18abea51d165cafddf70ee1019257))

### Fix
* Properly document and validate required OptionDefinition.location and OptionDefinition.domain attributes ([`ecb287e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ecb287e6af5143b15ded809974aea03331a52d21))
* Properly document and validate required OptionDefinition.location and OptionDefinition.domain attributes ([`14ea4e0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/14ea4e0679dc18035e4845ffcf2f6858320dfe90))
* Generate correct subdomains and collect all options for preflight option ([`2a9bfeb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/2a9bfeb681e21e3bf09d3a1a33557210a5e70675))
* Filter invalid refs ([`217194b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/217194b874df5c1dcff785a00ad22b20c426df57))
* Match_by_selector should always return False if no objects match ([`131bd6b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/131bd6bf5f2da1766333bbff7f3f05bef012f8d1))
* Restore tests for select_by_XXX_reference ([`d21d72b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/d21d72bd5c959d38811b6d8cfab6e4346f7c5319))
* File-references class part is default ([`c9095d0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/c9095d06b03e49097b1d58de20544622331b8ea3))
* Swap "?" and (no oper) operations ([`92523b9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/92523b92ea44596c46b82261385ec57b3c704fed))
* Remove mod parsing from `parse_selector` ([`3b975fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/3b975fef5ae0e0fa96e35b4caee81c739983db95))
* Only raise InvalidDependencies for explicit dependencies, not for wildcard or placeholder ones ([`50f54ac`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/50f54acc44899f0d3987a3585cca3a61be302651))
* Correct providers for tasks@scheduler value ([`5a5c803`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/5a5c8034b563c282641efeddf307eff8535b1997))
* Change default pre-flight error action to 'error' ([`ea21419`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/ea21419a31f49e919961fa95afec8213aeb8a605))
* For 'sum', 'min' and 'max' modifier, cast items to numbers ([`77fd72e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/77fd72ec052a99d6f4bfb7c663a8d5818a9e0411))
* With task numbers available, step option is no longer needed ([`a5b898f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/a5b898fcad77e5e81f7822fa1660d62dbede978f))
* Make VALID_LOCATIONS a set ([`70b2dd6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/70b2dd692520d1795c951aad24a4b0f4a4e692df))
* Remove unused function ([`46762aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/46762aa0b93a4101492f6ea12db48bbbb3ac10c1))
* Refs have multiple id's, but only a single class/name part; return all elements even if there's no match (needed for match selector) ([`17c47fa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/17c47fa7ae03bfe9644bfc5cd0025a002b20cea8))
* Conditions as part of selectors can contain '#' ([`9c47283`](https://gitlab.tue.nl/momotor/engine-py3/momotor-engine-options/-/commit/9c47283eb75e63b5465bc51e9fe27b8d9e8b04c9))
