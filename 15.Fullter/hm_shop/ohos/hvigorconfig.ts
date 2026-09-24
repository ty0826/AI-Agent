import fs from 'fs';
import path from 'path';
import { hvigor } from '@ohos/hvigor';

// Hvigor requires forward-slash relative paths, including on Windows.
const dependenciesFile = path.join(path.dirname(__dirname), '.flutter-plugins-dependencies');
if (fs.existsSync(dependenciesFile)) {
    const dependencies = JSON.parse(fs.readFileSync(dependenciesFile, 'utf8'));
    for (const plugin of dependencies.plugins?.ohos ?? []) {
        if (plugin.native_build === false) {
            continue;
        }
        let srcPath = path.relative(__dirname, path.resolve(plugin.path, 'ohos'));
        if (path.isAbsolute(srcPath)) {
            throw new Error(
                `Flutter plugin ${plugin.name} is on another drive. ` +
                'Set PUB_CACHE to the same drive as this project, restart your IDE, ' +
                'and run flutter pub get again.'
            );
        }
        srcPath = srcPath.split(path.sep).join('/');
        hvigor.getHvigorConfig().includeNode(
            plugin.name, srcPath.startsWith('.') ? srcPath : `./${srcPath}`
        );
    }
}
