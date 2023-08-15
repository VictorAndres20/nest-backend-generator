export class HttpResponse<T>{

    private ok: boolean;
    private msg: string;
    private error: string;
    private data: T;
    private list: T[];
    private paged: [T[], number];

    setError(error: string): HttpResponse<T>{
        this.error = error;
        return this;
    }

    setMessage(msg: string): HttpResponse<T>{
        this.msg = msg;
        return this;
    }

    setData(data: T): HttpResponse<T>{
        this.data = data;
        return this;
    }

    setList(list: T[]): HttpResponse<T>{
        this.list = list;
        return this;
    }

    setPaged(paged: [T[], number]): HttpResponse<T>{
        this.paged = paged;
        return this;
    }

    build(status: boolean){
        this.ok = status;
        return this;
    }

}