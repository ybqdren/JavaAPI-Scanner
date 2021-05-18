package com.alibaba.fastjson;

public abstract class JSON implements JSONStreamAware, JSONAware {

    private static final ConcurrentHashMap<Type, Type> mixInsMapper = new ConcurrentHashMap<Type, Type>(16);

    static {
        int features = 0;
        features |= Feature.AutoCloseSource.getMask();
        features |= Feature.InternFieldNames.getMask();
        features |= Feature.UseBigDecimal.getMask();
        features |= Feature.AllowUnQuotedFieldNames.getMask();
        features |= Feature.AllowSingleQuotes.getMask();
        features |= Feature.AllowArbitraryCommas.getMask();
        features |= Feature.SortFeidFastMatch.getMask();
        features |= Feature.IgnoreNotMatch.getMask();
        DEFAULT_PARSER_FEATURE = features;
    }


    private static void config(Properties properties) {
        {
            String featuresProperty = properties.getProperty("fastjson.serializerFeatures.MapSortField");
            int mask = SerializerFeature.MapSortField.getMask();
            if ("true".equals(featuresProperty)) {
                DEFAULT_GENERATE_FEATURE |= mask;
            } else if ("false".equals(featuresProperty)) {
                DEFAULT_GENERATE_FEATURE &= ~mask;
            }
        }

        {
            if ("true".equals(properties.getProperty("parser.features.NonStringKeyAsString"))) {
                DEFAULT_PARSER_FEATURE |= Feature.NonStringKeyAsString.getMask();
            }
        }

        {
            if ("true".equals(properties.getProperty("parser.features.ErrorOnEnumNotMatch"))
                    || "true".equals(properties.getProperty("fastjson.parser.features.ErrorOnEnumNotMatch")))
            {
                DEFAULT_PARSER_FEATURE |= Feature.ErrorOnEnumNotMatch.getMask();
            }
        }

        {
            if ("false".equals(properties.getProperty("fastjson.asmEnable"))) {
                ParserConfig.global.setAsmEnable(false);
                SerializeConfig.globalInstance.setAsmEnable(false);
            }
        }
    }
