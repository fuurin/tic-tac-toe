import axios from 'axios';

export class TTT {
    constructor(private baseURL: string) {}
    
    public bot(board: string[][], callback: (data: any) => void) {
        axios.get(`${this.baseURL}/bot`, {
            params: { board: JSON.stringify(board), }
        })
        .then((res: any) => {
            callback(res.data);
        });
    }
}