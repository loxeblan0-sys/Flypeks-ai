import { mysqlTable, varchar, datetime } from 'drizzle-orm/mysql-core';

export const users = mysqlTable('users', {
  id: varchar('id', { length: 256 }).primaryKey(),
  name: varchar('name', { length: 256 }),
  email: varchar('email', { length: 256 }).unique(),
  createdAt: datetime('created_at').defaultNow(),
});
