'use client';

import styles from "./page.module.css";

export default function SocketTest() {
  return (
    <div className={styles.container}>
      <h1>Socket.IO Client</h1>
      <input
        type="text"
        id="messageInput"
        className={styles.messageInput}
        placeholder="Enter a message"
      />
      <button id="sendButton" className={styles.sendButton}>
        Send
      </button>
      <ul id="messages" className={styles.messagesList}></ul>
    </div>
  );
}
