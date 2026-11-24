// Client-side TypeScript definitions
export type TaskStatus = 'BACKLOG' | 'TODO' | 'IN_PROGRESS' | 'CODE_REVIEW' | 'DONE';
export type TaskPriority = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export interface TaskCard {
  id: string;
  issueKey: string;
  title: string;
  priority: TaskPriority;
  status: TaskStatus;
  assigneeName?: string;
  spentHours: number;
  remainingHours: number;
}
