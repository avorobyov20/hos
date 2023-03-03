const config = {
  "branches": [
    "master"
  ],
  "ci": true,
  "debug": true,
  "dryRun": false,
  "tagFormat": "${version}",
  "preset": "conventionalcommits",
  "githubUrl": "https://api.github.com",
  "verifyConditions": [
    "@semantic-release/changelog",
    "@semantic-release/git",
    "@semantic-release/github"
  ],
  "analyzeCommits": [
    {
      "path": "@semantic-release/commit-analyzer",
      "releaseRules": [
        {
          "breaking": true,
          "release": "major"
        },
        {
          "type": "build",
          "release": "patch"
        },
        {
          "type": "chore",
          "release": false
        },
        {
          "type": "ci",
          "release": false
        },
        {
          "type": "docs",
          "release": "patch"
        },
        {
          "type": "feat",
          "release": "minor"
        },
        {
          "type": "fix",
          "release": "patch"
        },
        {
          "type": "perf",
          "release": "patch"
        },
        {
          "type": "refactor",
          "release": false
        },
        {
          "type": "revert",
          "release": "patch"
        },
        {
          "type": "style",
          "release": false
        },
        {
          "type": "test",
          "release": false
        }
      ]
    }
  ],
  "generateNotes": [
    {
      "path": "@semantic-release/release-notes-generator",
      "writerOpts": {
        "groupBy": "type",
        "commitGroupsSort": "title",
        "commitsSort": "header"
      },
      "linkCompare": true,
      "linkReferences": true,
      "presetConfig": {
        "types": [
          {
            "type": "build",
            "section": "🦊 CI/CD",
            "hidden": false
          },
          {
            "type": "chore",
            "section": "🔨 Прочие изменения",
            "hidden": false
          },
          {
            "type": "ci",
            "section": "🦊 CI/CD",
            "hidden": false
          },
          {
            "type": "docs",
            "section": "📔 Документация",
            "hidden": false
          },
          {
            "type": "example",
            "section": "📝 Примеры",
            "hidden": false
          },
          {
            "type": "feat",
            "section": "🚀 Новые функции",
            "hidden": false
          },
          {
            "type": "fix",
            "section": "🛠 Исправления",
            "hidden": false
          },
          {
            "type": "perf",
            "section": "⏩ Улучшения"
          },
          {
            "type": "refactor",
            "section": "✂️ Рефакторинг",
            "hidden": false
          },
          {
            "type": "revert",
            "section": "🙅‍♂️  Отмененные изменения"
          },
          {
            "type": "style",
            "section": "💈 Стилевые правки"
          },
          {
            "type": "test",
            "section": "🧪 Тестирование",
            "hidden": false
          }
        ],
        "issueUrlFormat": "https://github.com/yourlogin/yourrepo/issues/{{id}}"
      }
    }
  ],
  "prepare": [
    {
      "path": "@semantic-release/exec",
      "prepareCmd": 'echo "version=\"${nextRelease.version}\"\nrelease_url=\"https://github.com/yourlogin/yourrepo/releases/tag/${nextRelease.version}\"\nrelease_date=${new Date().toISOString()}" > version.toml'
    },
    {
      "path": "@semantic-release/changelog"
    },
    {
      "path": "@semantic-release/git",
      "message": 'Релиз: ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      "assets": [
        "CHANGELOG.md",
        "version.toml"
      ]
    }
  ],
  "publish": [
    {
      "path": "@semantic-release/github"
    }
  ],
  "success": false,
  "fail": false
};

module.exports = config;
