function _base64ToArrayBuffer(base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}

function _arrayBufferToBase64( buffer ) {
  var binary = '';
  var bytes = new Uint8Array( buffer );
  var len = bytes.byteLength;
  for (var i = 0; i < len; i++) {
     binary += String.fromCharCode( bytes[ i ] );
  }
  return window.btoa( binary );
}

document.addEventListener("DOMContentLoaded", function() {
    var old_prefilter = jQuery.htmlPrefilter;

    jQuery.htmlPrefilter = function(v) {

        var regs = [
            /<a[^>]*href="(?<url>[^"]*)"[^>]*>/gi,
            /<img[^>]*src="(?<url>[^"]*)"\/?>/gi,
            /<source[^>]*src="(?<url>[^"]*)"/gi
        ];

        var replaces = {};

        for (i in regs)
        {
            reg = regs[i];

            var m = true;
            var n = 0;
            while (m && n < 100)
            {
                n += 1;

                m = reg.exec(v);
                if (m)
                {
                    if (m['groups'] && m['groups']['url'])
                    {
                        var url = m['groups']['url'];
                        if (server_data.hasOwnProperty(url))
                        {
                            console.log(`Added url:${url} to be replaced with data of ${server_data[url].length} bytes length`);
                            replaces[url] = server_data[url];                                    
                        }
                    }
                }
            }
        }

        for (let src in replaces)
        {
            let dest = replaces[src];
            v = v.replace(src, dest);
        }

        return old_prefilter(v);
    };
});

var server_data="{{jsondata}}";
var server = sinon.fakeServer.create();
server.autoRespond = true;

"{{responses}}"
