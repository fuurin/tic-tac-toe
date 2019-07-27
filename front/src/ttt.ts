import axios from 'axios';

export class TTT {
    constructor(private baseURL: string) {}

    public init(callback: (data: any) => void) {
        axios.get(this.baseURL)
        .then((res: any) => {
            callback(res.data);
        });
    }

    public move(row: number, col: number, callback: (data: any) => void) {
        axios.get(`${this.baseURL}/move?row=${row}&col=${col}`)
        .then((res: any) => {
            callback(res.data);
        });
    }

    public bot(board: string[][], callback: (data: any) => void) {
        axios.get(`${this.baseURL}/bot`, {
            params: { board: JSON.stringify(board), }
        })
        .then((res: any) => {
            callback(res.data);
        });
    }
}