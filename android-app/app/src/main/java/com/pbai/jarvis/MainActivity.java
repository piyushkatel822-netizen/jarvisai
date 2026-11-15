package com.pbai.jarvis;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.*;
import android.widget.Toast;

public class MainActivity extends Activity {
    private WebView webView;
    private PermissionRequest pendingPermission;
    private ValueCallback<Uri[]> fileCallback;

    private static final int AUDIO_REQUEST = 101;
    private static final int FILE_REQUEST = 102;

    private static final String HOME =
        "https://piyushkatel822-netizen.github.io/jarvisai/";

    private static final String TRUSTED_HOST =
        "piyushkatel822-netizen.github.io";

    private boolean isTrustedOrigin(Uri uri) {
        return uri != null
            && "https".equalsIgnoreCase(uri.getScheme())
            && TRUSTED_HOST.equalsIgnoreCase(uri.getHost());
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(true);
        settings.setSupportZoom(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);

        CookieManager.getInstance().setAcceptCookie(true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(
                WebView view, WebResourceRequest request
            ) {
                Uri uri = request.getUrl();

                if (!request.isForMainFrame()) {
                    return false;
                }

                if (isTrustedOrigin(uri)) {
                    return false;
                }

                if (uri != null &&
                    ("https".equalsIgnoreCase(uri.getScheme()) ||
                     "http".equalsIgnoreCase(uri.getScheme()))) {
                    try {
                        startActivity(new Intent(
                            Intent.ACTION_VIEW, uri
                        ));
                    } catch (Exception e) {
                        Toast.makeText(
                            MainActivity.this,
                            "Cannot open external link",
                            Toast.LENGTH_SHORT
                        ).show();
                    }
                }
                return true;
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                runOnUiThread(() -> {
                    if (!isTrustedOrigin(request.getOrigin())) {
                        request.deny();
                        return;
                    }

                    String[] resources = request.getResources();
                    boolean audioOnly = resources.length > 0;

                    for (String resource : resources) {
                        if (!PermissionRequest.RESOURCE_AUDIO_CAPTURE
                                .equals(resource)) {
                            audioOnly = false;
                        }
                    }

                    if (!audioOnly) {
                        request.deny();
                        return;
                    }

                    if (checkSelfPermission(Manifest.permission.RECORD_AUDIO)
                            == PackageManager.PERMISSION_GRANTED) {
                        request.grant(new String[]{
                            PermissionRequest.RESOURCE_AUDIO_CAPTURE
                        });
                    } else {
                        pendingPermission = request;
                        requestPermissions(
                            new String[]{Manifest.permission.RECORD_AUDIO},
                            AUDIO_REQUEST
                        );
                    }
                });
            }

            @Override
            public boolean onShowFileChooser(
                WebView view,
                ValueCallback<Uri[]> callback,
                FileChooserParams params
            ) {
                if (fileCallback != null) {
                    fileCallback.onReceiveValue(null);
                }

                fileCallback = callback;

                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("image/*");

                try {
                    startActivityForResult(
                        Intent.createChooser(intent, "Choose an image"),
                        FILE_REQUEST
                    );
                } catch (Exception e) {
                    fileCallback = null;
                    callback.onReceiveValue(null);
                    Toast.makeText(
                        MainActivity.this,
                        "Cannot open image picker",
                        Toast.LENGTH_SHORT
                    ).show();
                }
                return true;
            }
        });

        webView.loadUrl(HOME);
    }

    @Override
    public void onRequestPermissionsResult(
        int requestCode, String[] permissions, int[] results
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, results);

        if (requestCode == AUDIO_REQUEST && pendingPermission != null) {
            if (results.length > 0 &&
                results[0] == PackageManager.PERMISSION_GRANTED) {
                pendingPermission.grant(new String[]{
                    PermissionRequest.RESOURCE_AUDIO_CAPTURE
                });
            } else {
                pendingPermission.deny();
            }
            pendingPermission = null;
        }
    }

    @Override
    protected void onActivityResult(
        int requestCode, int resultCode, Intent data
    ) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == FILE_REQUEST && fileCallback != null) {
            Uri result = (resultCode == RESULT_OK && data != null)
                ? data.getData() : null;

            fileCallback.onReceiveValue(
                result == null ? null : new Uri[]{result}
            );
            fileCallback = null;
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        if (pendingPermission != null) {
            pendingPermission.deny();
            pendingPermission = null;
        }

        if (fileCallback != null) {
            fileCallback.onReceiveValue(null);
            fileCallback = null;
        }

        if (webView != null) {
            webView.destroy();
            webView = null;
        }

        super.onDestroy();
    }
}
