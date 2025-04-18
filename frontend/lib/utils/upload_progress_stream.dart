import 'dart:async';

class UploadProgressStream extends Stream<List<int>> {
  final Stream<List<int>> _stream;
  final void Function(int bytesSent) onProgress;
  int _sent = 0;
  final int totalBytes;

  UploadProgressStream(this._stream, this.totalBytes, this.onProgress);

  @override
  StreamSubscription<List<int>> listen(
    void Function(List<int> data)? onData, {
    Function? onError,
    void Function()? onDone,
    bool? cancelOnError,
  }) {
    return _stream.listen(
      (chunk) {
        _sent += chunk.length;
        onProgress(_sent);
        if (onData != null) {
          onData(chunk);
        }
      },
      onError: onError,
      onDone: onDone,
      cancelOnError: cancelOnError,
    );
  }
}
