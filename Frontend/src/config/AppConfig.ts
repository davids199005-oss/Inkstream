export class AppConfig {
    static readonly BASE_URL = 'http://localhost:8000/api'
    static readonly CONVERSATIONS_PATH = `${this.BASE_URL}/conversations`
    static readonly CONVERSATION_PATH = `${this.BASE_URL}/conversations/:id`
    static readonly MESSAGES_PATH = `${this.BASE_URL}/conversations/:id/messages`
    static readonly MESSAGE_PATH = `${this.BASE_URL}/conversations/:id/messages/:messageId`
    static readonly MESSAGE_CREATE_PATH = `${this.BASE_URL}/conversations/:id/messages`
    static readonly MESSAGE_UPDATE_PATH = `${this.BASE_URL}/conversations/:id/messages/:messageId`
    static readonly MESSAGE_DELETE_PATH = `${this.BASE_URL}/conversations/:id/messages/:messageId`
}

export const appConfig = new AppConfig()