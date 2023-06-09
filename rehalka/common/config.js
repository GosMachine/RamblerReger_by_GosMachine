var Config = {

    default: {
        isPluginEnabled: true,
        apiKey: null,
        valute: "USD",
        email: null,
        autoSubmitForms: true,
        submitFormsDelay: 0,
        enabledForNormal: false,
        enabledForRecaptchaV2: false,
        enabledForInvisibleRecaptchaV2: false,
        enabledForRecaptchaV3: false,
        enabledForHCaptcha: true,
        enabledForGeetest: false,
        enabledForKeycaptcha: false,
        enabledForArkoselabs: false,
        autoSolveNormal: false,
        autoSolveRecaptchaV2: false,
        autoSolveInvisibleRecaptchaV2: false,
        autoSolveRecaptchaV3: false,
        recaptchaV3MinScore: 0.5,
        autoSolveHCaptcha: true,
        autoSolveGeetest: false,
        autoSolveKeycaptcha: false,
        autoSolveArkoselabs: false,
        repeatOnErrorTimes: 0,
        repeatOnErrorDelay: 0,
        useProxy: false,
        proxytype: "HTTP",
        proxy: "",
        normalSources: [],
        autoSubmitRules: [{
            url_pattern: "(2|ru)captcha.com/demo",
            code: "" +
                '{"type":"source","value":"document"}' + "\n" +
                '{"type":"method","value":"querySelector","args":["button[type=submit]"]}' + "\n" +
                '{"type":"method","value":"click"}',
        }],
    },

    get: async function (key) {
        let config = await this.getAll();
        return config[key];
    },

    getAll: function () {
        return new Promise(function(resolve, reject) {
            chrome.storage.local.get('config', function (result) {
                resolve(Config.joinObjects(Config.default, result.config));
            });
        });
    },

    set: function (newData) {
        return new Promise(function(resolve, reject) {
            Config.getAll()
                .then(data => {
                    chrome.storage.local.set({
                        config: Config.joinObjects(data, newData)
                    }, function (config) {
                        resolve(config);
                    });
                });
        });
    },

    joinObjects: function (obj1, obj2) {
        let res = {};
        for (let key in obj1) res[key] = obj1[key];
        for (let key in obj2) res[key] = obj2[key];
        return res;
    },

};
