var DATA;

function togglePassword() {
    var c = $('#userpass');
    console.log(c), c.attr('type', this.checked ? 'text' : 'password')
}

function togglePin() {
    var c = $('#userpin');
    c.attr('type', this.checked ? 'password' : 'number'), c.attr('disabled', !!this.checked)
}

function registerSuccessful(c) {
    try {
        if (!c.success) return registerError(c.error)
    } catch (d) {
        return console.log(d), registerError()
    }
    $('#success-text').html('Welcome <b>' + $('#username').val() + '</b>! Your account has been successfully registered! You can now play and explore the game! <br> To get your penguin name as the username you set, you must authenticate yourself by following the emai sent to <b>' + $('#useremail').val() + '</b> from <b>support@timeline</b>'), $('#register').remove(), $('#success').fadeIn(), $('#ovloader, #overlay-loader').fadeOut()
}

function registerError(c) {
    if ($('#errors').fadeIn(), $('#demo-toast-example')[0].MaterialSnackbar.showSnackbar({
            timeout: 1e4,
            actionHandler: function() {},
            actionText: 'View Errors',
            message: 'Registration Failed :-(. Please correct the errors and try again!'
        }), grecaptcha.reset(), !c || !c.length) return $('#error-list').html('Something went wrong! Please try again or contact support.'), void $('#ovloader, #overlay-loader').fadeOut();
    for (var f = $('#error-list'), g = 0; g < c.length; g++) {
        var h = '<li class="mdl-list__item mdl-list__item--three-line"> <span class="mdl-list__item-primary-content"> <i class="material-icons mdl-list__item-icon">person</i> <span>{ERROR_COLUMN}</span> <span class="mdl-list__item-text-body"> {ERROR_TEXT} </span> </span> <span class="mdl-list__item-secondary-content"> <a class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white" href="#{ERROR_ELEMENT}">Go there</a> </span> </li>'.format({
                ERROR_COLUMN: c[g].title,
                ERROR_ELEMENT: c[g].ref,
                ERROR_TEXT: c[g].msg
            }),
            j = $(h);
        j.appendTo(f)
    }
    $('#ovloader, #overlay-loader').fadeOut()
}

function onRecaptcha(c) {
    post = {
        recaptcha: c
    }, $.ajax({
        type: 'post',
        url: '//localhost:2083/register/' + DATA,
        data: {
            recaptcha: c
        },
        success: registerSuccessful,
        error: registerError
    })
}

function register() {
    var c = $('#ovloader, #overlay-loader');
    c.fadeIn();
    var g = ['username', 'userpass', 'useremail', 'userpin', 'usernick', 'usercolor'].map(l => {
            return $.base64.encode($('#' + l).val())
        }),
        h = ['ismember', 'userterms'].map(l => {
            return $.base64.encode($('#' + l)[0].checked ? '1' : '0')
        }),
        j = g.concat(h),
        k = j.join(';');
    DATA = $.base64.encode(k), console.info('msg: ' + DATA), $('#errors').fadeOut(), $('#error-list').html(''), $('.g-recaptcha').trigger('click')
}

function _() {
    $('#showpassd').change(togglePassword), $('#hidepin').change(togglePin), $('input').attr('required', '1'), $('#signupsubmit').on('click', register)
}
$(document).ready(function() {
    console.log('Timeline.SignUp::ready.'), _()
}), String.prototype.format = function(c) {
    return this.replace(/{([^{}]*)}/g, function(d, f) {
        var g = c[f];
        return 'string' == typeof g || 'number' == typeof g ? g : d
    })
};
 function MaterialSelect(t) {"use strict"; this.element_ = t, this.maxRows = this.Constant_.NO_MAX_ROWS, this.init() } MaterialSelect.prototype.Constant_ = {NO_MAX_ROWS: -1, MAX_ROWS_ATTRIBUTE: "maxrows"}, MaterialSelect.prototype.CssClasses_ = {LABEL: "mdl-textfield__label", INPUT: "mdl-select__input", IS_DIRTY: "is-dirty", IS_FOCUSED: "is-focused", IS_DISABLED: "is-disabled", IS_INVALID: "is-invalid", IS_UPGRADED: "is-upgraded"}, MaterialSelect.prototype.onKeyDown_ = function(t) {"use strict"; var s = t.target.value.split("\n").length; 13 === t.keyCode && s >= this.maxRows && t.preventDefault() }, MaterialSelect.prototype.onFocus_ = function(t) {"use strict"; this.element_.classList.add(this.CssClasses_.IS_FOCUSED) }, MaterialSelect.prototype.onBlur_ = function(t) {"use strict"; this.element_.classList.remove(this.CssClasses_.IS_FOCUSED) }, MaterialSelect.prototype.updateClasses_ = function() {"use strict"; this.checkDisabled(), this.checkValidity(), this.checkDirty() }, MaterialSelect.prototype.checkDisabled = function() {"use strict"; this.input_.disabled ? this.element_.classList.add(this.CssClasses_.IS_DISABLED) : this.element_.classList.remove(this.CssClasses_.IS_DISABLED) }, MaterialSelect.prototype.checkValidity = function() {"use strict"; this.input_.validity.valid ? this.element_.classList.remove(this.CssClasses_.IS_INVALID) : this.element_.classList.add(this.CssClasses_.IS_INVALID) }, MaterialSelect.prototype.checkDirty = function() {"use strict"; this.input_.value && this.input_.value.length > 0 ? this.element_.classList.add(this.CssClasses_.IS_DIRTY) : this.element_.classList.remove(this.CssClasses_.IS_DIRTY) }, MaterialSelect.prototype.disable = function() {"use strict"; this.input_.disabled = !0, this.updateClasses_() }, MaterialSelect.prototype.enable = function() {"use strict"; this.input_.disabled = !1, this.updateClasses_() }, MaterialSelect.prototype.change = function(t) {"use strict"; t && (this.input_.value = t), this.updateClasses_() }, MaterialSelect.prototype.init = function() {"use strict"; this.element_ && (this.label_ = this.element_.querySelector("." + this.CssClasses_.LABEL), this.input_ = this.element_.querySelector("." + this.CssClasses_.INPUT), this.input_ && (this.input_.hasAttribute(this.Constant_.MAX_ROWS_ATTRIBUTE) && (this.maxRows = parseInt(this.input_.getAttribute(this.Constant_.MAX_ROWS_ATTRIBUTE), 10), isNaN(this.maxRows) && (this.maxRows = this.Constant_.NO_MAX_ROWS)), this.boundUpdateClassesHandler = this.updateClasses_.bind(this), this.boundFocusHandler = this.onFocus_.bind(this), this.boundBlurHandler = this.onBlur_.bind(this), this.input_.addEventListener("input", this.boundUpdateClassesHandler), this.input_.addEventListener("focus", this.boundFocusHandler), this.input_.addEventListener("blur", this.boundBlurHandler), this.maxRows !== this.Constant_.NO_MAX_ROWS && (this.boundKeyDownHandler = this.onKeyDown_.bind(this), this.input_.addEventListener("keydown", this.boundKeyDownHandler)), this.updateClasses_(), this.element_.classList.add(this.CssClasses_.IS_UPGRADED))) }, MaterialSelect.prototype.mdlDowngrade_ = function() {"use strict"; this.input_.removeEventListener("input", this.boundUpdateClassesHandler), this.input_.removeEventListener("focus", this.boundFocusHandler), this.input_.removeEventListener("blur", this.boundBlurHandler), this.boundKeyDownHandler && this.input_.removeEventListener("keydown", this.boundKeyDownHandler) }, componentHandler.register({constructor: MaterialSelect, classAsString: "MaterialSelect", cssClass: "mdl-js-select", widget: !0 }); "use strict"; jQuery.base64 = (function($) {var _PADCHAR = "=", _ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", _VERSION = "1.0"; function _getbyte64(s, i) {var idx = _ALPHA.indexOf(s.charAt(i)); if (idx === -1) {throw "Cannot decode base64"} return idx } function _decode(s) {var pads = 0, i, b10, imax = s.length, x = []; s = String(s); if (imax === 0) {return s } if (imax % 4 !== 0) {throw "Cannot decode base64"} if (s.charAt(imax - 1) === _PADCHAR) {pads = 1; if (s.charAt(imax - 2) === _PADCHAR) {pads = 2 } imax -= 4 } for (i = 0; i < imax; i += 4) {b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12) | (_getbyte64(s, i + 2) << 6) | _getbyte64(s, i + 3); x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 255, b10 & 255)) } switch (pads) {case 1: b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12) | (_getbyte64(s, i + 2) << 6); x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 255)); break; case 2: b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12); x.push(String.fromCharCode(b10 >> 16)); break } return x.join("") } function _getbyte(s, i) {var x = s.charCodeAt(i); if (x > 255) {throw "INVALID_CHARACTER_ERR: DOM Exception 5"} return x } function _encode(s) {if (arguments.length !== 1) {throw "SyntaxError: exactly one argument required"} s = String(s); var i, b10, x = [], imax = s.length - s.length % 3; if (s.length === 0) {return s } for (i = 0; i < imax; i += 3) {b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8) | _getbyte(s, i + 2); x.push(_ALPHA.charAt(b10 >> 18)); x.push(_ALPHA.charAt((b10 >> 12) & 63)); x.push(_ALPHA.charAt((b10 >> 6) & 63)); x.push(_ALPHA.charAt(b10 & 63)) } switch (s.length - imax) {case 1: b10 = _getbyte(s, i) << 16; x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 63) + _PADCHAR + _PADCHAR); break; case 2: b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8); x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 63) + _ALPHA.charAt((b10 >> 6) & 63) + _PADCHAR); break } return x.join("") } return {decode: _decode, encode: _encode, VERSION: _VERSION } }(jQuery));