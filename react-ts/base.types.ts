export interface HttpResponse<E> {
  ok?: boolean;
  error?: string;
  data?: E | null;
  list?: E[] | null;
  paged?: [E[], number];
}
