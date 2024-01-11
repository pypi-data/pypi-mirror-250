import { WEBSOCKET_API_URL } from '../utils/constants';
import { NotebookTags } from '../utils/types';

export class WebsocketManager {
  constructor() {
    this._socket = null;
    this._ongoingConnectionInfo = null;

    this._pingInterval = 540000; // 9min (AWS disconnects after 10min idle)
    this._pingTimer = null;
  }

  private _createSocket(connectionInfo: NotebookTags) {
    this._socket = new WebSocket(
      `${WEBSOCKET_API_URL}?conType=STUDENT&nbId=${connectionInfo.notebookId}&usrId=${connectionInfo.instanceId}`
    );

    this._socket.addEventListener('open', () => {
      console.log('WebSocket connection opened for', connectionInfo);

      this._startPingTimer();
    });

    this._socket.addEventListener('message', event => {
      const message = JSON.parse(event.data);
      if (message.action === 'BLA BLA BLA') {
        // process the message
      }
      console.log('Received message from server:', message);
      // Handle messages from the server
    });

    this._socket.addEventListener('close', event => {
      console.log('WebSocket connection closed for ', connectionInfo, event);

      this._stopPingTimer();
    });

    this._socket.addEventListener('error', event => {
      console.error('WebSocket error', event);
    });
  }

  public establishSocketConnection(connectionInfo: NotebookTags | null) {
    // if there is already a connection, close it and set the socket to null
    this._closeSocketConnection();

    this._ongoingConnectionInfo = connectionInfo;

    if (!connectionInfo) {
      return;
    }
    this._createSocket(connectionInfo);
  }

  // close the connection without resetting connection info in case the connection is closed with setting change
  private _closeSocketConnection() {
    if (this._socket) {
      this._socket.close();
    }
    this._socket = null;
  }

  // terminate connection when a panel is disposed/switched, reset connection info
  public terminateSocketConnection() {
    this._closeSocketConnection();
    this._ongoingConnectionInfo = null;
  }

  private _startPingTimer() {
    this._pingTimer = window.setInterval(() => {
      if (this._socket && this._socket.readyState === WebSocket.OPEN) {
        this._socket.send('{ "action":"ping" }');
      }
    }, this._pingInterval);
  }

  private _stopPingTimer() {
    if (this._pingTimer) {
      clearInterval(this._pingTimer);
      this._pingTimer = null;
    }
  }

  private _socket: WebSocket | null;
  private _ongoingConnectionInfo: NotebookTags | null;
  private _pingInterval: number;
  private _pingTimer: number | null;
}
